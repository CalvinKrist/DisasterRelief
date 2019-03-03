function updateSearchPage() {
	searchTextBox = document.getElementById("searchRequestBox");
	searchQuery   = searchTextBox.value();
	
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "api/searchWeb", true);
	xhr.onload = function (e) {
	  if (xhr.readyState === 4) {
		if (xhr.status === 200) {
		  console.log(xhr.responseText);
		} else {
		  console.error(xhr.statusText);
		}
	  }
	};
	xhr.onerror = function (e) {
	  console.error(xhr.statusText);
	};
	xhr.send(null);
}