function changeCities(region) {
    $.ajax({
        url: "../retrieve_cities.py",
        // context: document.body,
        data: {"region": region},
        success: function(response){
            alert(response);
        }
    });

    // var selectedValue = region;
    
}

