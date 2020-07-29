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

    //fetch the data
    this.appService.getTrials(this.p)
      .subscribe((data: any[]) => {
        //load the data
        this.trials = data;

        //hide the spinner
        this.bSpin = false;
    }, error => {
      //log the error
      console.log(error);

      //error
      this.strError = 'Oops: Something went wrong.  Please try again later.';

      //hide the spinner
      this.bSpin = false;
    });
  }

  //clear for a new search
  newSearch() {
    //reset trials
    this.trials = [];
    //reset participant data
    this.p = new Participant();
  }

  //navigate to the trial ID
  navigate(id) {
    window.open('https://www.cancer.gov/about-cancer/treatment/clinical-trials/search/v?&id=' + id);
  }

}
