import { Component, AfterViewInit, ElementRef, ViewChild, OnInit, ViewChildren, QueryList } from '@angular/core';
import axios from 'axios';
import User from './User'
import { GatePass } from './gate-pass';
import { GateDiffence } from './gate-difference';
import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController, LineElement, PointElement, LineController, ChartTypeRegistry } from 'chart.js';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCoffee } from '@fortawesome/free-solid-svg-icons';
import { faAngleDown } from '@fortawesome/free-solid-svg-icons';
import { faAngleUp } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-show-result',
  templateUrl: './show-result.component.html',
  styleUrls: ['./show-result.component.scss'],
})
export class ShowResultComponent implements OnInit, AfterViewInit{
  faCoffee = faCoffee;
  faAngleDown = faAngleDown;
  faAngleUp = faAngleDown;
  @ViewChild('chartAfterTesting', { static: false }) private chartAfterTesting!: ElementRef;
  @ViewChild('chartHistory', { static: false }) private chartHistory!: ElementRef;
  @ViewChildren('testingChart') testingChart!: QueryList<any>;
  @ViewChildren('historyChart') historyChart!: QueryList<any>;
  response : string | null = null;
  user_list : User[] = [];
  selectedUser : User | null = null;
  gatePass : GatePass[] = [];
  gateDifference : GateDiffence[] = [];
  sesija : number = 1;
  uniqueDates : Date[] = [];
  uniqueSession : number[] = [];
  sessionInProcess : boolean = false;
  myChart: Chart | undefined;
  showChart : boolean = false;
  indexChart : number[]= [];
  chartInstanceAfterTesting! : Chart;
  chartInstanceHistory! : Chart;
  chartIntanceForHistory : Chart[] = [];
  userIsSelected = false;
  showHistoryButton = true; 

  ngOnInit() : void
  {
    this.getAllUsers();
  }
  ngAfterViewInit(): void {
  }
  callFlask()
  {
    axios.post("http://localhost:5000/api/message", {message : "Pozdrav!"})
    .then(res =>
      {
        this.response = "Client connected!"
      })
    .catch(err =>
      {
        alert(err)
      });
  }
  async getAllUsers()
  {
    if(this.chartIntanceForHistory.length > 0)
      {
        this.indexChart = [];
        this.chartIntanceForHistory.forEach(chart =>
        {
          if(chart)
          {
            chart.destroy();
          }
        })
      }
    try
    {
      const resposne = await axios.get("http://localhost:5000/api/get-all-user")
      this.user_list = resposne.data['response']
    }
    catch (error)
    {
      alert(error)
    }
  }

  chooseUser(id : number)
  {
    this.showHistoryButton = true;
    if(this.chartIntanceForHistory.length > 0)
    {
      this.indexChart = [];
      this.chartIntanceForHistory.forEach(chart =>
      {
        if(chart)
        {
          chart.destroy();
        }
      })
    }
    this.gateDifference = [];
    this.gatePass = [];
    if (this.user_list.length !== 0)
    {
      this.selectedUser = this.user_list.find(e => e.id === id)!
      this.userIsSelected = true;
    }
    else
    {
      alert("There is no user with id: " + id)
      this.selectedUser = null
      this.userIsSelected = false;
    }
  }

  sendIdSelectedUser(id : number)
  {
    axios.post("http://localhost:5000/api/selected-user", {"id" : id})
    .then(res=>
      {
        alert(res.data.response)
      })
      .catch(err=>
        {
          alert(err)
        })
  }

  async getGatePassDataHistory(selectedUser : number)
  {
    this.showChart = false;
    this.gatePass = [];
    this.uniqueSession = [];
    this.gateDifference = [];
    this.showHistoryButton = false;

    if (this.chartAfterTesting)
      {
        if(this.chartInstanceAfterTesting)
        {
          this.chartInstanceAfterTesting.destroy()
        }
      }
    try
    {
      this.gateDifference = [];
      this.gatePass = [];
      const response = await axios.get(`http://localhost:5000/api/gate-pass-data/${selectedUser}`)
      let ui = response.data['response']
      this.gatePass = ui
      this.gatePass = this.gatePass.reverse();
      let ui1 = response.data['difference']
      this.gateDifference = ui1;
      this.uniqueDates = Array.from(new Set(this.gatePass.map(ele => ele.datum_testiranja)))
      this.uniqueSession = Array.from(new Set(this.gatePass.map(ele => ele.sesija)))
    }
    catch(err)
    {
      alert(err)
    }
  }

  newTestingCard()
  {
    this.showChart = false;
    this.gatePass = [];
    this.uniqueSession = [];
    this.gateDifference = [];
    this.showHistoryButton = true;

    if (this.chartAfterTesting)
    {
      if(this.chartInstanceAfterTesting)
      {
        this.chartInstanceAfterTesting.destroy()
      }
    }
  }

  historyTestingCard()
  {
    this.showChart = false;
    this.gatePass = [];
    this.uniqueSession = [];
    this.gateDifference = [];
    this.showHistoryButton = true;

    if (this.chartAfterTesting)
    {
      if(this.chartInstanceAfterTesting)
      {
        this.chartInstanceAfterTesting.destroy()
      }
    }
  }

  formatDate(gatePasss : Date)
  { 
    let gatePass = new Date(gatePasss) 
    let year = gatePass.getFullYear();
    let month = gatePass.getMonth() + 1;
    let day = gatePass.getDate();
    let hour = gatePass.getUTCHours();
    let minutes = gatePass.getMinutes();
    let secodns = gatePass.getSeconds();
    let miliseconds = gatePass.getMilliseconds();
   
    let gatePassFormated = `${year}-${month}-${day} ${hour}:${minutes}:${secodns}`;
    return gatePassFormated
  }

  formatDateWithoutTime(gatePasss : Date)
  { 
    let gatePass = new Date(gatePasss) 
    let year = gatePass.getFullYear();
    let month = gatePass.getMonth() + 1;
    let day = gatePass.getDate();
  
    let gatePassFormated = `${year}-${month}-${day}`;
    return gatePassFormated
  }

  startNewSession(userId : number)
  {
    if(this.chartIntanceForHistory.length > 0)
      {
        this.indexChart = [];
        this.chartIntanceForHistory.forEach(chart =>
        {
          if(chart)
          {
            chart.destroy();
          }
        })
      }
    if (this.chartAfterTesting)
      {
        if(this.chartInstanceAfterTesting)
        {
          this.chartInstanceAfterTesting.destroy()
        }
      }
    this.showChart = false;
    this.sessionInProcess = true;
    this.gateDifference = [];
    this.gatePass = [];
    axios.post("http://localhost:5000/api/start-test", {"userId" : userId, "session" : this.sesija})
    .then(res=>
      {
        this.sessionInProcess = true;
      })
    .catch(err =>
    {
      alert(err)
    })
  }
  async endNewSession(userId : number)
  {
    this.sessionInProcess = false;
    const response = await axios.post('http://localhost:5000/api/finish-test' ,{"userId": userId, "session" : this.sesija})
    this.gatePass = response.data['response']
    this.gatePass = this.gatePass.reverse();
    this.gateDifference = response.data['difference'];
    this.uniqueDates = Array.from(new Set(this.gatePass.map(ele => ele.datum_testiranja)))
    this.uniqueSession = Array.from(new Set(this.gatePass.map(ele => ele.sesija)))
    this.sessionInProcess = false;
    this.showChart = true;
    this.createChartAfterSession()
    this.sesija = 1;

  }

  createChart(index : number, gatePassChart : Date,sessionNumberChart : number) {

    let gateDif : GateDiffence[] = this.getGateDifferences(gatePassChart, sessionNumberChart);

    let dataForChart = [];
    let labelsForChart = [];
    dataForChart = gateDif.filter(ele=> ele.gateForChart=='1').map(ele => ele.difference).reverse();
    labelsForChart = gateDif.filter(ele=> ele.gateForChart=='1').map(ele=> ele.gate.replace(ele.gate, ele.gate.split(":")[0].concat(":" + ele.gate.split(":")[1].trim().split("-").reverse().join("-")))).reverse();
    
    let typeChart  = gateDif.length > 1 ? 'line' as keyof ChartTypeRegistry : 'bar' as keyof ChartTypeRegistry;

    if (this.indexChart.length == 0)
    {
      this.indexChart.push(index)
    }
    else
    {
      if(this.indexChart.includes(index))
      {
        let lastEle = this.indexChart[this.indexChart.length-1] + 1
        index = lastEle
        this.indexChart.push(lastEle)
      }else
      {
        this.indexChart.push(index)
      }
    }

    Chart.register(
      Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController,
      LineElement, PointElement, LineController
    );

    const canvas = this.testingChart.toArray()[index].nativeElement;
    const ctx = canvas.getContext('2d')//this.neca.nativeElement.getContext('2d');
    if (canvas.chart) {
      canvas.chart.destroy();
    }

    const chart =  new Chart(ctx, {
        type: typeChart,  // Now this is valid because BarController is registered
        data: {
          labels: labelsForChart,
          datasets: [{
            label: 'My Dataset',
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',],
            data: dataForChart
          }]
        },
        options: {
          responsive: true
        }
      });

    this.chartIntanceForHistory.push(chart);

  }

  getGateDifferences(testingDate: Date, session : number) : GateDiffence[]
  {
    let gateDifferencess = this.gateDifference.filter(ele=> ele.dateTesting == testingDate && ele.session == session)
    return gateDifferencess
  }

  createChartAfterSession()
  {
    let dataForChart = [];
    let labelsForChart = [];

    dataForChart = this.gateDifference.filter(ele=> ele.gateForChart=='1').map(ele => ele.difference).reverse();
    labelsForChart = this.gateDifference.filter(ele=> ele.gateForChart=='1').map(ele=> ele.gate.replace(ele.gate, ele.gate.split(":")[0].concat(":" + ele.gate.split(":")[1].trim().split("-").reverse().join("-")))).reverse();
    let gate1 : string = labelsForChart[0]
    let yu = gate1.split(":")
    let typeChart  = this.gateDifference.length > 1 ? 'line' as keyof ChartTypeRegistry : 'bar' as keyof ChartTypeRegistry;
    let backgroundColorsPicker = [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(255, 192, 203,0.2)',
      'rgba(255, 182, 193,0.2)',
      'rgba(255, 140, 0, 0.2)',
      'rgba(255, 165, 0, 0.2)']
    let backgroundColors = []
    for (let  i = 0; i < dataForChart.length; i++)
    {
      let ind = Math.floor(Math.random() * (backgroundColorsPicker.length - 0 + 1)) + 0
      backgroundColors.push(backgroundColorsPicker[ind])
    }
    
    Chart.register(
      Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController,
      LineElement, PointElement, LineController
    );

    const ctx = this.chartAfterTesting.nativeElement.getContext('2d');
    this.chartInstanceAfterTesting = new Chart(ctx, {
      type: typeChart,  
      data: {
        labels: labelsForChart,
        datasets: [{
          label: 'My Dataset',
          backgroundColor: backgroundColors,
          data: dataForChart
        }]
      },
      options: {
        responsive: true
      }
    });
  }
  createChartHistorySession()
  {
    let dataForChart = [];
    let labelsForChart = [];
    
    dataForChart = this.gateDifference.filter(ele=> ele.gateForChart=='1').map(ele => ele.difference).reverse();
    labelsForChart = this.gateDifference.filter(ele=> ele.gateForChart=='1').map(ele=> ele.gate.replace(ele.gate, ele.gate.split(":")[0].concat(":" + ele.gate.split(":")[1].trim().split("-").reverse().join("-")))).reverse();
    let gate1 : string = labelsForChart[0]
    let yu = gate1.split(":")
    let typeChart  = this.gateDifference.length > 1 ? 'line' as keyof ChartTypeRegistry : 'bar' as keyof ChartTypeRegistry;
    let backgroundColorsPicker = [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(255, 192, 203,0.2)',
      'rgba(255, 182, 193,0.2)',
      'rgba(255, 140, 0, 0.2)',
      'rgba(255, 165, 0, 0.2)']
    let backgroundColors = []
    for (let  i = 0; i < dataForChart.length; i++)
    {
      let ind = Math.floor(Math.random() * (backgroundColorsPicker.length - 0 + 1)) + 0
      backgroundColors.push(backgroundColorsPicker[ind])
    }
    
    Chart.register(
      Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController,
      LineElement, PointElement, LineController
    );

    const ctxH = this.chartHistory.nativeElement.getContext('2d');
    this.chartInstanceHistory = new Chart(ctxH, {
      type: typeChart,  
      data: {
        labels: labelsForChart,
        datasets: [{
          label: 'My Dataset',
          backgroundColor: backgroundColors,
          data: dataForChart
        }]
      },
      options: {
        responsive: true
      }
    });
  }

  createChartHistory(index : number, gatePassChart : Date,sessionNumberChart : number) {

    let gateDif : GateDiffence[] = this.getGateDifferences(gatePassChart, sessionNumberChart);
    
    let dataForChart = [];
    let labelsForChart = [];
    dataForChart = gateDif.filter(ele=> ele.gateForChart=='1').map(ele => ele.difference).reverse();
    labelsForChart = gateDif.filter(ele=> ele.gateForChart=='1').map(ele=> ele.gate.replace(ele.gate, ele.gate.split(":")[0].concat(":" + ele.gate.split(":")[1].trim().split("-").reverse().join("-")))).reverse();
    
    let typeChart  = gateDif.length > 1 ? 'line' as keyof ChartTypeRegistry : 'bar' as keyof ChartTypeRegistry;

    if (this.indexChart.length == 0)
    {
      this.indexChart.push(index)
    }
    else
    {
      if(this.indexChart.includes(index))
      {
        let lastEle = this.indexChart[this.indexChart.length-1] + 1
        index = lastEle
        this.indexChart.push(lastEle)
      }else
      {
        this.indexChart.push(index)
      }
    }
    Chart.register(
      Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController,
      LineElement, PointElement, LineController
    );

    const canvas = this.historyChart.toArray()[index].nativeElement;
    const ctx = canvas.getContext('2d')
    if (canvas.chart) {
      canvas.chart.destroy();
    }
    const chart =  new Chart(ctx, {
        type: typeChart, 
        data: {
          labels: labelsForChart,
          datasets: [{
            label: 'My Dataset',
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',],
            data: dataForChart
          }]
        },
        options: {
          responsive: true
        }
      });
  }
}
