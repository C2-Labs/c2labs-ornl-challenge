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
export class PatientsComponent implements OnDestroy {


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
    console.log(this.p);
    this.appService.getTrials(this.p).pipe(takeUntil(this.destroy$)).subscribe((trials: any[]) => {
      this.trials = trials;
      console.log(trials);
    });
    
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }
}
