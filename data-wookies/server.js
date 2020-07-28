const express = require('express');
const app = express(),
      bodyParser = require("body-parser");
      port = 3000;

const path = require('path')
const {spawn, ChildProcess} = require('child_process');
const SCRIPT_PATH = path.join(__dirname, 'scripts/get-trials.py')

app.use(bodyParser.json());
app.use(express.static(process.cwd()+"/client/dist/data-wookies/"));

app.post('/api/trials', (req, res) => {
    const gender = req.body.participant['gender'];
    const age = req.body.participant['age'];
    const zipcode = req.body.participant['zipcode'];
    const distance = req.body.participant['distance'];
    const cancerType = req.body.participant['cancerType'];
    const cancerStage = req.body.participant['cancerStage'];
    const cancerSite = req.body.participant['keywords'];

    const child = runScript(gender, age, zipcode, distance, cancerType, cancerSite, cancerStage)
    console.log("Script Started");
    child.stdout.on('data', (data) => {
        try {
            res.json(JSON.parse(data.toString("utf8")));
        } catch (error) {
            res.json(error);
        }
      });
      child.stderr.on('data', (data) => {
        console.log(`error:\n${data}`);
      });
      child.on('close', () => {
        console.log("Script Ended");
      });
});

app.get('/', (req,res) => {
    res.sendFile(process.cwd()+"/client/dist/data-wookies/index.html");
});

app.get('/home', (req,res) => {
    res.sendFile(process.cwd()+"/client/dist/data-wookies/index.html");
});

app.get('/patients', (req,res) => {
    res.sendFile(process.cwd()+"/client/dist/data-wookies/index.html");
});

app.get('/providers', (req,res) => {
    res.sendFile(process.cwd()+"/client/dist/data-wookies/index.html");
});

app.get('/visualizations', (req,res) => {
    res.sendFile(process.cwd()+"/client/dist/data-wookies/index.html");
});

app.get('/docs', (req,res) => {
    res.sendFile(process.cwd()+"/client/dist/data-wookies/index.html");
});


app.listen(port, () => {
    console.log(`Server listening on the port::${port}`);
});

/**
 * @param param {String}
 * @return {ChildProcess}
 */
function runScript(gender, age, zipcode, distance, cancerType, cancerSite, cancerStage) {
    /*
    python -u get-trials.py --participant
    */
    return spawn('python3', [
      "-u", SCRIPT_PATH,
      gender,
      age,
      zipcode,
      distance,
      cancerType,
      cancerSite,
      cancerStage,
    ]);
  }