import puppeteer from 'puppeteer';
import { ResourceClient } from 'utils/js/resource_client';

// class WeightsAndBiasesClient extends ResourceClient {

//     async getResources(){
//         const browser = await puppeteer.launch();
//         const [page] = await browser.pages();
//         page.on('response', async (response) => {
//             if(response.url() == "https://api.wandb.ai/graphql" && response.status() == 200){
//                 const data = await response.json();
//                 if (data && data.data && data.data.views && data.data.views.edges) {
//                     const posts = data.data.views.edges
//                 } 
//             }
//         })
//         await page.goto(this.url, { waitUntil: 'networkidle0' });
//     }    
// }


const url = "https://wandb.ai/fully-connected";

(async () => {
    const browser = await puppeteer.launch({headless: false});
    const [page] = await browser.pages();
    page.on('response', async (response) => {
        if(response.url() == "https://api.wandb.ai/graphql" && response.status() == 200){
            const data = await response.json();
            if (data && data.data && data.data.views && data.data.views.edges) {
                const posts = data.data.views.edges
                console.log(posts);
            } 
        }
    })

    await page.goto(url, { waitUntil: 'networkidle0' });
    await browser.close();
})();


