import React from 'react';
import ReactDOM from 'react-dom';
import * as jsPDF from 'jspdf';
import * as xmldom from 'xmldom';
import './index.css';

class FormTitle extends React.Component {
	render() {
		return (
			<div class="title">
				<h1>PLATA REGIE CAMIN</h1>
			</div>
		);
	}
}

class SmartForm extends React.Component {
	constructor(props) {
    	super(props);

	    this.state = {
	    	firstName: '', 
	    	lastName: '',
	    	email: '',
	    	cnp: '',
	    	birthdate: '',
	    	camin: '',
	    	room: '',
	    	floor: 0,
	    	pay: [{month: '', sum: 0, extra: 0}],
	    	total: 0
	    };

	    this.handleChange = this.handleChange.bind(this);
	    this.handleSubmit = this.handleSubmit.bind(this);
	    this.completeBirthDate = this.completeBirthDate.bind(this);
	    this.completeAddress = this.completeAddress.bind(this);
	    this.handleAddPayMonth = this.handleAddPayMonth.bind(this);
	    this.selectMonthPay = this.selectMonthPay.bind(this);
	    this.computeTotal = this.computeTotal.bind(this);
	    this.generatePDF = this.generatePDF.bind(this);
	    this.generateRaport = this.generateRaport.bind(this);
  	}

	handleAddPayMonth() {
    	this.setState({
      		pay: this.state.pay.concat([{month: '', sum: 0, extra: 0}])
    	});
  	}

  	handleChange(event) {
  		const target = event.target;
  		const value = target.value;
  		const name = target.name;

  		this.setState({
  			[name]: value
  		});
	}

	validationEmail(email) {
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    	return re.test(String(email).toLowerCase());
	}

	validationCNP(cnp) {
		return cnp.length === 13 && cnp.match(/^-{0,1}\d+$/) != null;
	}

	validationCamin(camin) {
		var re = /^P[0-2][0-9]*/;
		return re.test(camin);
	}

	validationRoom(room) {
		return room.length === 3 && room.match(/[0-5][0-9][0-9]/) != null;
	}

	validationName(name) {
		var re = /^[A-Z][A-Za-z]+$/;
		return re.test(name);
	}

	completeBirthDate(event) {
		const cnp = event.target.value;
		const year = (parseInt(cnp.substr(1, 2)) <= 18 && parseInt(cnp.substr(1, 2)) >= 0) ? "20" + cnp.substr(1, 2) : "19" + cnp.substr(1, 2);
		const month = cnp.substr(3, 2);
		const day = cnp.substr(5, 2);

		this.setState({
			birthdate: day + ' ' + month + ' ' + year
		});
	}

	completeAddress(event) {
		const room = event.target.value;
		const floor = parseInt(room.substr(0, 1));

		this.setState({
			floor: floor
		});
	}

	selectMonthPay(event) {
		var pay = this.state.pay;
		var total = this.state.total;
		const length = Object.keys(this.state.pay).length; 
		const monthToPay = event.target.value;

		var extra = 0;
		var months = ["Luna", "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
		var sum = {"Ianuarie": 175, "Februarie": 175, "Martie": 165, "Aprilie": 150, "Mai": 150, "Iunie": 135, "Iulie": 300, "August": 300, "Septembrie": 150, "Octombrie": 165, "Noiembrie": 175, "Decembrie": 175}
		
		const today = new Date();
		const day = today.getDate();
		const month = today.getMonth() + 1;
		const year = today.getFullYear();
		
		if (month - months.indexOf(monthToPay) >= 1) {
			extra += sum[monthToPay];
		} else {
			if (day > 15) {
				extra += 0.3 * sum[monthToPay] * (day - 15) / 100;
			}
		}

		pay[length - 1].month = monthToPay;
		pay[length - 1].sum = sum[monthToPay];
		pay[length - 1].extra = extra;

		total += pay[length - 1].sum + pay[length - 1].extra;

		this.setState({
			pay: pay,
			total: total
		})
	}

	computeTVA(sum) {
		return sum * 19 / 100;
	}

	computeTotal() {
		var total = 0;
		var pay = this.state.pay;

		for (var p in pay) {
			total += pay[p].sum + pay[p].extra;
		}

		return total;
	}

	generatePDF() {
    	const data = {
    		"firstName": this.state.firstName,
    		"secondName": this.state.lastName,
    		"email": this.state.email,
    		"cnp": this.state.cnp,
    		"birthdate": this.state.birthdate,
    		"camin": this.state.camin,
    		"room": this.state.room,
    		"floor": this.state.floor,
    		"pay": this.state.pay,
    		"total": this.state.total
    	}

	    const pdf = new jsPDF();
		const today = new Date();
		const day = today.getDate();
		const month = today.getMonth() + 1;
		const year = today.getFullYear();

	    pdf.text(70, 10, 'ORDIN DE PLATA');
	    pdf.text(10, 30, 'Data facturare ' + day + ' ' + month + ' ' + year);
	    pdf.text(10, 50, 'CLIENT');
	    pdf.text(10, 60, data['firstName'] + ' ' + data['secondName']);
	    pdf.text(10, 70, data['cnp'] + '');
	    pdf.text(10, 80, data['email']+ '');
	    pdf.text(10, 120, 'Adresa');
	    pdf.text(10, 130, 'Camin ' + data['camin'] + ', etaj ' + data['floor'] + ', camera ' + data['room']);
	    pdf.text(10, 160, 'PLATI REGIE CAMIN')

	    var lastPos = 170;
	    pdf.text(10, lastPos, 'Luna');
	    pdf.text(60, lastPos, 'Suma');
	    pdf.text(110, lastPos, 'Penalizare');
	    pdf.text(160, lastPos, 'Total');
	    for (var p in data['pay']) {
	    	lastPos += 10;
	    	var pay = data['pay'][p];
	    	pdf.text(10, lastPos, pay.month + ' ' + year)
	    	pdf.text(60, lastPos, pay.sum + '');
	    	pdf.text(110, lastPos, pay.extra+ '');
	    	pdf.text(160, lastPos, (pay.sum + pay.extra) + '');
	    }
	    pdf.text(140, lastPos + 30, 'TOTAL ' + data['total'] + ' lei');

	    pdf.save('ordin_de_plata.pdf');
	}

    generateRaport() {
    	    fetch("http://127.0.0.1:5000/raport", {
	  		method: 'POST',
	  		headers: {
	    		'Accept': 'application/json',
	    		'Content-Type': 'application/json',
	  		},
	  		body: 'raport'
		});
    }

	generateXML(data) {
	 	var form = document.getElementsByTagName("form");
	 	const xmlDoc = new DOMParser().parseFromString(form, "application/xml");

    	const upload = new FormData();
    	upload.append('file', xmlDoc);
		upload.append('filename', 'xmlForm.xml');

	 	fetch("http://127.0.0.1:5000/xml", {
	  		method: 'POST',
	  		body: upload
		});
	}

  	handleSubmit(event) {
  		if (!this.validationName(this.state.firstName)) {
  			alert("Numele este incorect");
    		event.preventDefault();
  		}
  		if (!this.validationName(this.state.lastName)) {
  			alert("Prenumele este incorect");
    		event.preventDefault();
  		}
  		if (!this.validationEmail(this.state.email)) {
  			alert("Adresa de mail este incorecta");
    		event.preventDefault();
  		}
  		if (!this.validationCNP(this.state.cnp)) {
  			alert("CNPul este incorect");
    		event.preventDefault();
  		}
  		if (!this.validationCamin(this.state.camin)) {
  			alert("Numarul caminului este incorect");
    		event.preventDefault();
  		}
  		if (!this.validationRoom(this.state.room)) {
  			alert("Camera este incorecta");
    		event.preventDefault();
  		}
    	
    	const data = {
    		"firstName": this.state.firstName,
    		"secondName": this.state.lastName,
    		"email": this.state.email,
    		"cnp": this.state.cnp,
    		"birthdate": this.state.birthdate,
    		"camin": this.state.camin,
    		"room": this.state.room,
    		"floor": this.state.floor,
    		"pay": this.state.pay,
    		"total": this.state.total
    	}

    	event.preventDefault();

	    fetch("http://127.0.0.1:5000/", {
	  		method: 'POST',
	  		headers: {
	    		'Accept': 'application/json',
	    		'Content-Type': 'application/json',
	  		},
	  		body: JSON.stringify(data)
		});

		this.generateXML(data);
  }

  	render() {

		var num = [0, 1, 2, 3, 4, 5];
		var months = ["Luna", "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
		
    	return (

      	<form class='smartForm' onSubmit={this.handleSubmit} >
      	<div class="w3-card-4 personalInfo">
        	<p>
          		<label>Nume</label>
          		<input 
          			class="w3-input"
          			name="firstName"
          			type="text" 
          			value={this.state.firstName} 
          			onChange={this.handleChange} />
        	</p>
        	<p>
          		<label>Prenume</label>
          		<input 
          			class="w3-input"
          			name="lastName"
          			type="text" 
          			value={this.state.lastName} 
          			onChange={this.handleChange} />
        	</p>
        	<p>
        		<label>Email</label>
          		<input 
          			class="w3-input"
          			name="email"
          			type="text" 
          			value={this.state.email} 
          			onChange={this.handleChange} />
        	</p>
        	<p>
        		<label>CNP</label>
          		<input 
          			class="w3-input"
          			name="cnp"
          			type="text" 
          			value={this.state.cnp} 
          			onChange={this.handleChange}
          			onBlur={this.completeBirthDate} />
        	</p>
        	<p>
        		Data nasterii: {this.state.birthdate}
        	</p>
        </div>

        	<div class="w3-card-4 address">
        		<p>
	        		<label>Camin</label>
	        		<input
          				class="w3-input"
	        			name="camin"
	        			type="text"
	        			value={this.state.camin}
	        			onChange={this.handleChange} />
      			</p>
      			<p>
	        		<label>Camera</label>
	        		<input
          				class="w3-input"
	        			name="room"
	        			type="text"
	        			value={this.state.room}
	        			onChange={this.handleChange}
	        			onBlur={this.completeAddress} />
        		</p>
        		<p>
	        		<label>Etaj</label>
					<select class="w3-select" name="floors">
	  					{num.map(function(n) { 
	      					return (
	      						<option 
	      							name="floor"
	      							value={this.state.floor}
	      							selected={this.state.floor === n}
	      							onChange={this.handleChange}>
	      								{n}
	      						</option>
	      					);
	  					}, this)}
					</select>
				</p>
			</div>

			<div class="w3-card-4 payment">
				<h5>Selectati lunile pentru care doriti sa efectuati plata</h5>
			
			
        		{this.state.pay.map(function(month, idx) {
        			return (
          			<div>
						<select class="w3-select" name="monthsPay" onChange={this.selectMonthPay}>
  							{months.map(function(m) { 
      							return (
      								<option 
		      							name="pay"
		      							value={m} >
		      								{m} 
		      						</option>
		      					);
		  					}, this)}
						</select>

		      			<div class="payInfo">
		      				Suma de plata pentru luna {this.state.pay[idx].month}: {this.state.pay[idx].sum} lei <br />
		      				TVA: {this.computeTVA(this.state.pay[idx].sum)} lei <br />
		      				Penalizare: {this.state.pay[idx].extra} lei
		  				</div>
		          	</div>
		        	);
		     	}, this)}
        	<button 
        		class="w3-btn w3-yellow"
        		type="button" 
        		onClick={this.handleAddPayMonth} >
        		Adauga alta luna
        	</button>
        </div>

        <div class="w3-card-4 total">
        
        <button 
        	class="w3-btn w3-black paymentPdf"
        	type="button"
        	onClick={this.generatePDF} >
        	Genereaza ordin plata
        </button>
        <button 
        	class="w3-btn w3-black raportPdf"
        	type="button"
        	onClick={this.generateRaport} >
        	Genereaza raport
        </button>
       	<input class="w3-btn w3-black submit" type="submit" value="Plateste" />
        	<h4> Total de plata {this.computeTotal()} lei </h4>
        </div>


      	</form>
    	);
  	}
}

class MainComponent extends React.Component {
	render() {
		return (
			<div>
				<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css" />
				<FormTitle />
				<SmartForm />
			</div>
		);
	}
}

ReactDOM.render(
	<MainComponent />,
  	document.getElementById('root')
);
