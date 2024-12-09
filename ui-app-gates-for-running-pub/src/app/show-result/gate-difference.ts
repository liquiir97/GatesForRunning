
export class GateDiffence
{
    gate! : string;
    difference! : number;
    dateTesting! : Date;
    session! : number;
    gateForChart! : string;


    constructor(gate : string, difference : number, dateTesting : Date, session : number, gateForChart : string)
    {
        gate = gate;
        difference = difference;
        dateTesting = dateTesting;
        session = session;
        gateForChart = gateForChart
    }
}