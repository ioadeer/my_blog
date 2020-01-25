
var searchTextInput = document.getElementById("search-text-input");

searchTextInput.onkeydown = async function(evt){
	evt = evt || window.event;
	let query = searchTextInput.value;
 	let host = window.location.origin;
	if(query.length >= 3 || query != ""){
		let url = host + "/blog/ajax/search/?q="+query;
		let response  = await fetch(url);
		if(response.ok){
			let json_dict = await response.json();
			let arrayOfJSON = JSON.parse(json_dict);
			let authors = []; 
			let titles = [];
			for(let i = 0; i < arrayOfJSON.length; i++){
				authors.push(arrayOfJSON[i].author);
				titles.push(arrayOfJSON[i].title);
			}
			authors = authors.filter( onlyUnique ); 
			titles = titles.filter( onlyUnique ); 
			let authorAndTitles = authors.concat(titles);
			//autocomplete(searchTextInput, authorAndTitles);
			$( "#search-text-input" ).autocomplete({
      source:authorAndTitles 
    	});
		}
	}
}

/* function to filter distinct elements from array */
function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

