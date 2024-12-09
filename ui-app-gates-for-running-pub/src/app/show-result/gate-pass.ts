
export class GatePass
{
    id! : number;
    message! : string;
    user_id! : string;
    date_time_pass!  : Date;
    datum_testiranja! : Date;
    sesija! : number;

    constructor(id : number, message : string, user_id : string, date_time_pass : Date, datum_testiranja : Date, sesija : number)
    {
        id = id;
        message = message;
        user_id = user_id;
        date_time_pass = date_time_pass;
        datum_testiranja = datum_testiranja;
        sesija = sesija;
    }

}