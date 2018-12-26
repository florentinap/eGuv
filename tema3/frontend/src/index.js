import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';


class Pap extends React.Component {
	render() {
		return (
			<tr><td><a href={this.props.pap}>{this.props.pap}</a></td></tr>
		);
	};
}

class Minister extends React.Component {
	render() {
		return (
			<tr class='minister'>
				<td>{this.props.nume}</td>
				<td><a href={this.props.url}>{this.props.url}</a></td>
			</tr> 
		);
	};
}

class Ministere extends React.Component {
	constructor(props) {
    	super(props);

    	this.state = {
        	data: []
    	};

    	this.getData = this.getData.bind(this);
  	}

  	getData() {
  		var result = [];
  		fetch("http://127.0.0.1:5000/data", {
	  		method: 'GET'
		})
		.then(response => 
    		response.json().then(data => {
        		return data
    		}
		).then(res => {
    		result = res;
		}));

		return result;
  	}

   componentWillMount() {
   		var data = this.getData();
   		this.setState({data: data});
   }

	render() {
		var rows = [];
		this.state.data.forEach(function (item) {
			rows.push(<Minister nume={item.nume} url={item.url}/>);
			item.paps.forEach(function(papItem) {
				rows.push(<Pap pap={papItem}/>);
			})
			rows.push(<tr><td></td></tr>);
		});

		return (
			<div class="ministere">
				<h1>MINISTERE</h1>
				<table>
					<tbody>
						{rows}
					</tbody>
				</table>
			</div>
		);
	}
}


class MainComponent extends React.Component {
	render() {
		return (
			<div>
				<Ministere />
			</div>
		);
	}
}

ReactDOM.render(
	<MainComponent />,
  	document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
