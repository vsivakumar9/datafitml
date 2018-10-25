console.log("Displaying js")
$('#btnfile').on('change',function(){
                //get the file name
                var fileName = $(this).val();
                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            })
   

 var submit_element = document.getElementById("submit");
 var dropdown_element = document.getElementById("Algorithm");

submit_element.addEventListener('click',function(){
	
	switch (dropdown_element.value){
		case 'KNN':
			url = '/KNN';
			break;
		case 'Decision Tree':
			url = '/Decision_Tree';
			break;
	}
	let key,value;
	
	html_string = ''
	d3.json(url).then((data) =>{
		if (url == '/Decision_Tree')
		{
			renderDecisionTree(data);
		}

		else{
			renderDecisionTree(data['KNN_Metrics'])
		}
		console.log('Data Returned',data);
		
	},(error) => {
		console.log('Data Returned',error);
	})


})

 function renderDecisionTree(data){
	console.log(data)
	console.log(data["Decision Tree Score"])
	console.log(data["Feature Importance"])
	console.log(data["Random Forest Score"])

	var table = Plotly.d3.select("#data-from-server");
    var tbody = table.select("tbody");

	var data_list = [];
	
	var attr_c = ["Decision Tree Score","Random Forest Score"]

	for(var i =0; i <attr_c.length;i++){

		var model_name = attr_c[i]
		var model_score_1 = data[model_name]
		var model_score = parseFloat(model_score_1.toFixed(2))
		var model_row = [model_name,model_score]
		data_list.push(model_row);
		$("tbody").empty();
		var rows = tbody.selectAll('tr')
		.data(data_list)
		.enter()
		.append('tr')
		.html(function(d){
			return `<td>${d[0]}</td><td>${d[1]}</td>`
		})  

	  }


 	for (key in data){
			value = data[key];
			if (key == 'Feature Importance'){
				document.getElementById("features").innerHTML = "Feature Importance(in percentage)";
				value.forEach((element)=>{
					value1 = element[1];
					value2 = parseFloat(element[0].toFixed(2))
					html_template = `<div class="row"> <div class="col-md-6"> ${value1}</div><div class="col-md-6">${value2}</div></div>`	
					html_string += html_template
				})
			} 
			
			// else {
			// 	html_template = `<div class="row"> <div class="col-md-6"> ${key}</div><div class="col-md-6">${value}</div></div>`
			// 	html_string += html_template
			// }
			
		}
		let v = document.getElementById('features1');
		v.innerHTML = html_string;
	
 }