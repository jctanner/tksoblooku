const puppeteer = require('puppeteer');
const chalk = require('chalk');
const fs = require('fs');

const error = chalk.bold.red;
const success = chalk.keyword("green");

const width = 1920;
const height = 1280;


(async () => {

    console.log("starting run ...");

    try {

        console.log("opening browser ...");
        let browser = await puppeteer.launch({
            headless: true,
            ignoreHTTPSErrors: true,
            args: [`--window-size=${width},${height}`]
        });

        console.log("create new page ...");
        let page = await browser.newPage();
        page.setViewport({
            width: width,
            height: height
        });

        console.log("goto url ...");
        await page.goto('https://nine.websudoku.com/?level=4');
        console.log("waiting for selector ...");
        await page.waitForSelector("#puzzle_grid");
        
        console.log("save screenshot ...");
        await page.screenshot({path: 'board.png'});

        console.log("save html ...");
        let bodyHTML = await page.evaluate(() => document.body.innerHTML);
        fs.writeFile('page.html', bodyHTML, function (err) {});

        /*
        console.log("eval table ...");
        const pg_table = await page.evaluate(async () => {
            console.log("looking for grid ...");
            const table = await document.getElementById("puzzle_grid");
            console.log('table', table);

            for (let i = 0; i < table.children.lengh; i++) {
                //let child = table.children[i];
                console.log('child', table.children[i]);
            }

            return table;
        });
        console.log('pgtable', pg_table, pg_table.children);
        */

        const input_values = await page.evaluate(() => {
            const newInputs = document.querySelectorAll("#puzzle_grid > tbody > tr > td > input");
            //console.log('table', table);
            console.log('newinputs', newInputs, newInputs.length);

            let values = [];
            for (var i = 0; i < newInputs.length; i++ ) {
                values.push(newInputs[i].getAttribute("value"));
            }

            return values;
        });
        console.log('input values', input_values, input_values.length);
        const jData = JSON.stringify(input_values);
        console.log('jdata', jData);
        console.log("writing board.json ...");
        fs.writeFile('board.json', jData, function (err) {});

        console.log("closing browser ...");
        await browser.close();

    } catch (err) {
        console.log(error(err));
        //await browser.close();
    }
})();
