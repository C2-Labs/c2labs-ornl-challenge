import { DocumentationComponent } from './documentation/documentation.component';
import { VisualizationsComponent } from './visualizations/visualizations.component';
import { ProvidersComponent } from './providers/providers.component';
import { PatientsComponent } from './patients/patients.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';


const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'patients', component: PatientsComponent },
  { path: 'providers', component: ProvidersComponent },
  { path: 'visualizations', component: VisualizationsComponent },
  { path: 'docs', component: DocumentationComponent },
  { path: '', component: HomeComponent },
  { path: '**', component: HomeComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
