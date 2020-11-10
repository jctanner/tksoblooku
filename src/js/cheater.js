const puppeteer = require('puppeteer');
const chalk = require('chalk');
const fs = require('fs');
//const { exec } = require('child_process');
const exec = require('await-exec');

const error = chalk.bold.red;
const success = chalk.keyword("green");

const width = 1920;
const height = 1280;


(async () => {

    console.log("starting run ...");

    try {

        console.log("opening browser ...");
        let browser = await puppeteer.launch({
            headless: false,
            ignoreHTTPSErrors: true
            //args: [`--window-size=${width},${height}`]
        });

        console.log("create new page ...");
        let page = await browser.newPage();
        /*
        page.setViewport({
            width: width,
            height: height
        });
        */

        console.log("goto url ...");
        await page.goto('https://nine.websudoku.com/?level=4');
        console.log("waiting for selector ...");
        await page.waitForSelector("#puzzle_grid");
        
        console.log("save screenshot ...");
        await page.screenshot({path: 'board.png'});

        console.log("save html ...");
        let bodyHTML = await page.evaluate(() => document.body.innerHTML);
        fs.writeFile('page.html', bodyHTML, function (err) {});

        const input_values = await page.evaluate(() => {
            const inputs = document.querySelectorAll("#puzzle_grid > tbody > tr > td > input");
            console.log('inputs', inputs, inputs.length);
            let values = [];
            for (var i = 0; i < inputs.length; i++ ) {
                values.push(inputs[i].getAttribute("value"));
            }
            return values;
        });
        console.log('input values', input_values, input_values.length);
        const jData = JSON.stringify(input_values);
        console.log('jdata', jData);
        console.log("writing board.json ...");
        fs.writeFile('board.json', jData, function (err) {});

        ///////////////////////////////////
        // OPEN THE PY APP AND SOLVE IT !!!
        ///////////////////////////////////
        console.log('starting solver ...');
        await exec('python3 soblooku.py', (err, stdout, stderr) => {
            if (error) {
                console.log(error(err));
                return;
            }
            if (stderr) {
                console.log(stderr);
                return;
            }
        });

        ///////////////////////////////////
        // GET THE SOLUTION
        ///////////////////////////////////
        let sol = fs.readFileSync('solution.json');
        let jSol = JSON.parse(sol);

        ///////////////////////////////////
        // FILL IN THE ANSWER
        ///////////////////////////////////
        const input_ids = await page.evaluate(async () => {
            const inputs = document.querySelectorAll("#puzzle_grid > tbody > tr > td > input");
            let ids = []
            for (var i = 0; i < inputs.length; i++ ) {
                let thisid = inputs[i].getAttribute("id");
                let thisval = inputs[i].getAttribute("value");
                ids.push([thisid, thisval]);
            }
            return ids;
        });

        for (var i = 0; i < input_ids.length; i++ ) {
            console.log(i);
            console.log('\t' + input_ids[i][0]);
            console.log('\t' + input_ids[i][1]);
            console.log('\t' + jSol.vals[i]);
            if (input_ids[i][1] === null || input_ids[i][1] === "") {
                console.log('\t typing ...');
                await page.type('#' + input_ids[i][0], jSol.vals[i].toString());
            }
        };


        console.log("closing browser ...");
        await browser.close();

    } catch (err) {
        console.log(error(err));
        //await browser.close();
    }
})();
