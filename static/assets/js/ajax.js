function createSliders(response, from, to, id){
         var slider = {};
         var slider2 = {};
         slider['slider'+id] = document.getElementById('slider-experts');
         slider2['slider2'+id] = document.getElementById('slider-results');

         slider2['slider2'+id].setAttribute('disabled', true);

                noUiSlider.create(slider['slider'+id], {
                start: [parseFloat(from), parseFloat(to)],
                connect: true,
                    step: 0.1,
                 orientation: 'horizontal',
                    behaviour: "fixed",

                   range: {
                     'min': 0,
                     'max': 5
                   },
                   format: wNumb({
                     decimals: 1
                   })
                  });

                noUiSlider.create(slider2['slider2'+id], {
                start: [parseFloat(response)],
                connect: true,
                    step: 0.1,
                 orientation: 'horizontal',


                   range: {
                     'min': 0,
                     'max': 5
                   },
                     pips: {
                        mode: 'range',
                        density: 20
                    },
                   format: wNumb({
                     decimals: 1
                   })
                  });
var dot = $('#slider-experts .noUi-origin');

dot.addClass('noUi-origin2');
dot.removeClass('noUi-origin');
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    //CSRF token
    function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
    //Ajax calls
    function saveResponse(answer_id, response){
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
        });
        $.ajax({
            type: 'POST',
            url: '/save_response/'+answer_id+'/'+response
        })
        .done(function( data ) {
                $("#feedback_options").find('tbody').append('<tr><td>'+data.content+'</td><td>'+data.feedback+'</td><hr><p id="slider-experts"></p><p id="slider-results"></p></tr>');
                createSliders(response, data.from, data.to);
            });
    }
