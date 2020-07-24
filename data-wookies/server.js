const express = require('express');
const app = express(),
      bodyParser = require("body-parser");
      port = 3000;

const trials = [{"nci_id": "NCI-2009-00595", "nct_id": "NCT00719303", "title": "Diet and Physical Activity Change or Usual Care in Improving Progression-Free Survival in Patients with Previously Treated Stage II, III, or IV Ovarian, Fallopian Tube, or Primary Peritoneal Cancer", "location": "Wichita NCI Community Oncology Research Program", "contact_email": null, "contact_phone": "316-268-5374"}, {"nci_id": "NCI-2011-00878", "nct_id": "NCT00956007", "title": "Radiation Therapy with or without Cetuximab in Treating Patients Who Have Undergone Surgery for Locally Advanced Head and Neck Cancer", "location": "CoxHealth South Hospital", "contact_email": null, "contact_phone": "417-269-4520"}, {"nci_id": "NCI-2009-00603", "nct_id": "NCT00492778", "title": "Radiation Therapy with or without Cisplatin in Treating Patients with Recurrent Endometrial Cancer", "location": "Singing River Hospital", "contact_email": null, "contact_phone": "228-809-5292"}, {"nci_id": "NCI-2011-01915", "nct_id": "NCT00887146", "title": "Radiation Therapy or Radiation Therapy and Temozolomide in Treating Patients with Newly Diagnosed Anaplastic Glioma or Low Grade Glioma", "location": "Missouri Valley Cancer Consortium", "contact_email": "mwilwerding@mvcc.cc", "contact_phone": "402-991-8070ext202"}, {"nci_id": "NCI-2009-00336", "nct_id": "NCT00392327", "title": "Chemotherapy and Radiation Therapy in Treating Young Patients with Newly Diagnosed, Previously Untreated, High-Risk Medulloblastoma / PNET", "location": "Greenville Cancer Treatment Center", "contact_email": null, "contact_phone": "864-241-6251"}, {"nci_id": "NCI-2011-01972", "nct_id": "NCT00983697", "title": "Fludeoxyglucose F 18-PET / CT Imaging in Assessing the Tumor and Planning Neck Surgery in Patients with Newly Diagnosed Head and Neck Cancer", "location": "University of Washington Medical Center", "contact_email": null, "contact_phone": "206-616-8289"}, {"nci_id": "NCI-2011-00312", "nct_id": "NCT01012817", "title": "Veliparib and Topotecan Hydrochloride in Treating Patients with Solid Tumors, Relapsed or Refractory Ovarian Cancer, or Primary Peritoneal Cancer", "location": "Mayo Clinic in Arizona", "contact_email": null, "contact_phone": "855-776-0015"}, {"nci_id": "NCI-2011-02623", "nct_id": "NCT01272037", "title": "Tamoxifen Citrate, Letrozole, Anastrozole, or Exemestane with or without Chemotherapy in Treating Patients with Invasive RxPONDER Breast Cancer", "location": "Aspirus Regional Cancer Center", "contact_email": null, "contact_phone": "877-405-6866"}, {"nci_id": "NCI-2011-02599", "nct_id": "NCT01190930", "title": "Risk-Adapted Chemotherapy in Treating Younger Patients with Newly Diagnosed Standard-Risk Acute Lymphoblastic Leukemia or Localized B-Lineage Lymphoblastic Lymphoma", "location": "AdventHealth Orlando", "contact_email": "FH.Cancer.Research@flhosp.org", "contact_phone": "407-303-2090"}, {"nci_id": "NCI-2011-02611", "nct_id": "NCT01231906", "title": "Combination Chemotherapy in Treating Patients with Non-Metastatic Extracranial Ewing Sarcoma", "location": "Wayne State University / Karmanos Cancer Institute", "contact_email": null, "contact_phone": "313-576-9363"}]

const path = require('path')
const {spawn, ChildProcess} = require('child_process');
const SCRIPT_PATH = path.join(__dirname, 'scripts/script.py')

function runScript(){
    return spawn('python', [
          path.join(__dirname, './scripts/myscript.py'),
          '-foobar',
    ]);
}

app.use(bodyParser.json());
app.use(express.static(process.cwd()+"/client/dist/data-wookies/"));

app.post('/api/trials', (req, res) => {
    const child = runScript("foo", "bar")
    console.log("Script Started");
    console.log(req.body);
    child.stdout.on('data', (data) => {
        from_python = data.toString("utf8");
        console.log(from_python);
        res.json(from_python);
      });
      child.stderr.on('data', (data) => {
        console.log(`error:\n${data}`);
      });
      child.on('close', () => {
        console.log("Script Ended");
      });
});


app.listen(port, () => {
    console.log(`Server listening on the port::${port}`);
});

/**
 * @param param {String}
 * @return {ChildProcess}
 */
function runScript(param) {
    /*
    python -u script.py --foo bar
    */
    return spawn('python', [
      "-u", SCRIPT_PATH,
      "--foo", param,
    ]);
  }