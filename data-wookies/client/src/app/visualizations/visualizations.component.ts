import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-visualizations',
  templateUrl: './visualizations.component.html',
  styleUrls: ['./visualizations.component.css']
})
export class VisualizationsComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  //opens window for Kibana
  viewKibana(strView) {
    if (strView == 'maps') {
      window.open('https://datawookies-visualize.c2labs.com/app/maps#/?_g=()');
    } else if (strView == 'graphs') {
      window.open('https://datawookies-visualize.c2labs.com/app/kibana#/visualize?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))');
    }
    
  }

}
