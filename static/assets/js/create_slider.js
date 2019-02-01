function create_slider(item){
           var  class1 = 'slider-experts-' + item[0];
           var class2 = 'slider-results-' + item[2];
            $('#results').append(
                '                        <div class="row s12">\n' +
                '                                 <p >' + item[4] + '</p></div>\n' +
                '                        </div></br>\n' +
                 '                         <div class="row s12"><strong>You</strong>\n' +
                '                                <div class="' + class2 + '"></div></br></br>\n' +
                '                        </div>\n' +
                '                        <div class="row s12"><strong>Expert</strong>\n' +
                '                                <div class="' + class1 + '"></div></br></br>\n' +
                '                    </div>\n' +
                '                        <div class="row s12">\n' +
                '                                 <p>' + item[5] + '</p></div>\n' +
                '</br></br></br></br>');
            $('.' + class1).attr('id', item[0]);
            $('.' + class2).attr('id', item[2]);
            var s1 = document.getElementById(item[0]);
            var s2 = document.getElementById(item[2]);



        noUiSlider.create(s1, {
            start: item[1],
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
        var pipFormats = {'0':'Strongly disagree', '5':'Strongly agree'};
        noUiSlider.create(s2, {
            start: item[3],
            connect: true,
            step: 0.1,
            orientation: 'horizontal',


            range: {
                'min': 0,
                'max': 5
            },
            pips: {
                mode: 'range',
                format: {
                    to: function(a){
                    return pipFormats[a];
                        }
                    }
            }
        });
        s2.setAttribute('disabled', true);
        var dot = $('[class*="slider-experts"] .noUi-origin');
    dot.addClass('noUi-origin2');
    dot.removeClass('noUi-origin');
}