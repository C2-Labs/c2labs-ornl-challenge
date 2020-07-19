import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Participant } from './participant';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private http: HttpClient) { }

  rootURL = '/api';

  getTrials(participant: any) {
    console.log("getTrials Service Called");
    return this.http.post(this.rootURL + '/trials', {participant});
  }

}
