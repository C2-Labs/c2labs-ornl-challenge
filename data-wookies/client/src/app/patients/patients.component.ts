import { Participant } from './../participant';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { AppService } from '../app.service';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-patients',
  templateUrl: './patients.component.html',
  styleUrls: ['./patients.component.css']
})

export class PatientsComponent implements OnInit {


  //declare variables
  destroy$: Subject<boolean> = new Subject<boolean>();
  p = new Participant();
  trials: any[] = [];

  //inject services
  constructor(private appService: AppService) { }

  //initialize the components
  ngOnInit(): void {
  }

  //retrieve the list of trials
  getTrials() {
    this.appService.getTrials(this.p)
      .subscribe((data: any[]) => {
        this.trials = data;
    });
  }

  //clear for a new search
  newSearch() {
    this.trials = [];
  }

}
