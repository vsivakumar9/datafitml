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
 	for (key in data){
			value = data[key];
			if (key == 'Feature Importance'){
				value.forEach((element)=>{
					value1 = element[1];
					value2 = element[0];
					html_template = `<div class="row"> <div class="col-md-6"> ${value1}</div><div class="col-md-6">${value2}</div></div>`	
					html_string += html_template
				})
			} else {
				html_template = `<div class="row"> <div class="col-md-6"> ${key}</div><div class="col-md-6">${value}</div></div>`
				html_string += html_template
			}
			
		}
		let v = document.getElementById('data-from-server');
		v.innerHTML = html_string;


 }