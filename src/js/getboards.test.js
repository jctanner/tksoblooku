const puppeteer = require('puppeteer');

const width = 1920;
const height = 1280;


describe("getboards", () => {
    it("get random board", async () => {
		let browser = await puppeteer.launch({
			headless: true,
			ignoreHTTPSErrors: true,
			args: [`--window-size=${width},${height}`]
		});

		let page = await browser.newPage();
		page.setViewport({
			width: width,
			height: height
		});

        await page.goto('https://www.websudoku.com/?level=4');
        //await page.waitForNavigation()
        //await page.waitForTimeout(500);
        await page.screenshot({path: 'board.png'});

        /*
        await page.evaluate(async () => {
            const table = await document.querySelector("#puzzle_grid");
            console.log('table', table);

            for (let i = 0; i < table.children.lengh; i++) {
                let child = table.children[i];
            }

            return;
        });
        */

        /*
        const table = document.getElementById('puzzle_grid').innerHTML;
        */


        await browser.close();
    });
});
