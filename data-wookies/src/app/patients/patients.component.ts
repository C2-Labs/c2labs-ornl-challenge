import { Participant } from './../participant';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-patients',
  templateUrl: './patients.component.html',
  styleUrls: ['./patients.component.css']
})
export class PatientsComponent implements OnInit {

  //declare variables
  p = new Participant();

  //inject services
  constructor() { }

  //initialize the components
  ngOnInit(): void {
  }

  //retrieve the list of trials
  getTrials() {
    console.log(this.p);
  }

}
