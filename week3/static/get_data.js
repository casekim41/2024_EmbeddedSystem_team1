function distance_Data(){
    const warningSingal = document.querySelector('.notice_warning');
    warningSingal.classList.remove('active');

    var distance;
    
    $.ajax({
        url: '/get_distance',
        method: 'GET',
        success: function(data){
            console.log(data);
            distance = data.distance;
            $('.DIST_data').text(`${distance}cm`);
            console.log(data);
            if (distance < 30){
                warningSingal.classList.add('active');
            }

        }
    })
}

function touch_Data(){
    const autoBtn = document.querySelector('.auto_btn');
    const manuBtn = document.querySelector('.manu_btn');
    autoBtn.classList.remove('active');
    manuBtn.classList.remove('active');

    $.ajax({
        url: '/touch_state',
        method : 'GET',
        success: function(data){
            if (data.state == true){
                autoBtn.classList.add('active');
                manuBtn.classList.remove('active');
            }
            else{
                autoBtn.classList.remove('active');
                manuBtn.classList.add('active');
            }
        }
    })
}

function DHT_Data(){
    $.ajax({
        url: '/temp_humid',
        method: 'GET',
        success: function(data){
            
            temp = data.temp;
            humid = data.humid;
            
            $('.DHT_temp_data').text(`${temp}°C`);
            $('.DHT_humid_data').text(`${humid}%`);
        }
    })
}


window.onload = function(){
    setInterval(distance_Data, 3000);
    setInterval(DHT_Data, 3000);
    setInterval(touch_Data, 3000);
}

