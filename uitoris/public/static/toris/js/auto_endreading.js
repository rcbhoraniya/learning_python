    $("#id_plant").change(function () {
      var url = $("#plantproductionForm").attr("data-start-reading-url");  // get the url of the `load_cities` view
      var plantId = $(this).val();  // get the selected country ID from the HTML input
        console.log(plantId)
      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'plant': plantId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function

          $("#id_start_reading").attr("value", data);  // replace the contents of the city input with the data that came from the server
            console.log(data)
        }
      });

    });



