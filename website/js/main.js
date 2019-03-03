function updateSearchPage() {
	searchTextBox = document.getElementById("searchRequestBox");
	searchQuery   = searchTextBox.value;
	
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "https://hoos-disaster-relief.herokuapp.com/api/searchWeb", true);
	xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
		if (xhr.status === 200) {
		  responseBox = document.getElementById("searchResponse");
		  responseBox.innerHTML = xhr.responseText;
		} else {
		  console.error(xhr.statusText);
		}
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	xhr.send(searchQuery);
}