import { Participant } from './../participant';
import { Component, OnInit } from '@angular/core';
import { AppService } from '../app.service';

@Component({
  selector: 'app-patients',
  templateUrl: './patients.component.html',
  styleUrls: ['./patients.component.css']
})

export class PatientsComponent implements OnInit {


  //declare variables
  p = new Participant();
  trials: any[] = [];
  bSpin: boolean = false;
  bSearch: boolean = false;
  strError: string = '';

  //inject services
  constructor(private appService: AppService) { }

  //initialize the components
  ngOnInit(): void {
  }

  //retrieve the list of trials
  getTrials() {
    //show the spinner
    this.bSpin = true;

    //reset the error
    this.strError = '';

    //validation
    if (this.p.age <= 0) {
      this.strError += 'Error: Age must be greater than or equal to zero. ';
    } 
    if (this.p.cancerStage == '') {
      this.strError += 'Error: You must select a cancer stage. ';
    } 
    if (this.p.cancerType == null || this.p.cancerType == '') {
      this.strError += 'Error: You must enter one or more cancer types. ';
    } 
    if (this.p.distance <= 0) {
      this.strError += 'Error: Distance must be greater than or equal to zero. ';
    } 
    if (this.p.gender == '') {
      this.strError += 'Error: You must select a gender. ';
    } 
    if (this.p.keywords == '') {
      this.strError += 'Error: You must enter an anatomical site. ';
    } 
    if (this.p.zipcode == '') {
      this.strError += 'Error: You must enter a zip code. ';
    }

    //see if there are errors
    if (this.strError != '') {
      //hide the spinner
      this.bSpin = false;

      //error
      return;
    } else {
      //fetch the data
      this.appService.getTrials(this.p)
        .subscribe((data: any[]) => {
          //load the data
          this.trials = data;

          console.log(this.trials);
          console.log(this.trials.length);

          //hide the spinner
          this.bSpin = false;

          //flag search
          this.bSearch = true;
      }, error => {
        //log the error
        console.log(error);

        //error
        this.strError = 'Oops: Something went wrong.  Please try again later.';

        //hide the spinner
        this.bSpin = false;
      });
    }
  }

  //clear for a new search
  newSearch() {
    //reset trials
    this.trials = [];
    //reset participant data
    this.p = new Participant();
    //reset search flag
    this.bSearch = false;
  }

  //navigate to the trial ID
  navigate(id) {
    window.open('https://www.cancer.gov/about-cancer/treatment/clinical-trials/search/v?&id=' + id);
  }

}
