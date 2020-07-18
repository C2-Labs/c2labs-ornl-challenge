export class Participant {
    keywords: string;
    gender: string;
    zipcode: string;
    distance: number;
    age: number;
    cancerType: string;
    cancerStage: string;

    constructor() {
        this.keywords = '';
        this.gender = '';
        this.zipcode = '';
        this.distance = 0;
        this.age = 0;
        this.cancerType = '';
        this.cancerStage = '';
    }
}