const puppeteer = require('puppeteer');
const chalk = require('chalk');
const fs = require('fs');
const exec = require('await-exec');

const error = chalk.bold.red;
const success = chalk.keyword("green");

const width = 1920;
const height = 1280;


(async () => {

    console.log("starting run ...");

    try {

        ///////////////////////////////////
        // GET THE SOLUTION
        ///////////////////////////////////
        let sol = fs.readFileSync('solution.json');
        let jSol = JSON.parse(sol);
        console.log(jSol);

        for (let i = 0; i < jSol.vals.length; i++) {
            console.log(i);
            console.log('\t' + jSol.vals[i]);
        }

    } catch (err) {
        console.log(error(err));
        //await browser.close();
    }

})();
