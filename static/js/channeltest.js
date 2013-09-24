function showAlert(alertHTML) {
    $('#mainContainer').prepend($('<div class="alert"><button type="button" class="close" data-dismiss="alert">&times;</button>' + alertHTML + '</div>'));
}

function processNotification(messageObj) {     
     var dataObj = JSON.parse(messageObj.data);
     channelErrors = 0;
     
     // Insert new notification
     $('#topRow').after(dataObj.notificationHTML);
     
     // Update the number
     count = parseInt($('#notificationCount').text());
     count = count + 1;
     $('#notificationCount').text(count.toString());
     $('#notificationCount').show();
          
     // Insert the raised date secs value
     $('#notificationMenuHeader').data('latest', dataObj.timestamp);      
     
}

function notificationChannelOpen() {
    lastNotiSecs = $("#notificationMenuHeader").data('latest');
    channel = new goog.appengine.Channel(channelToken);
    socket = channel.open();
    socket.onmessage = processNotification;
    socket.onerror = function(errorObj) {
        if (errorObj.code != 0 ) {
            showAlert('Error in noti channel was: ' + errorObj.description + ' Code: ' + errorObj.code);                            
        }
    };
    socket.onclose = handleChannelError;    
}

function handleChannelError(errorObj) {  
    if (channelErrors > 2) {
        showAlert('Cannot receive notifications. Error was: ' + errorObj.description + ' Code: ' + errorObj.code);        
    } else {
        try {
            channelErrors = channelErrors + 1;            
        } catch (err) {
            alert(err.message);
        }
        try {
            $.ajaxSetup({
           		url: "/newNotificationChannel",
           		global: false,
           		type: "POST",           		
                success: function(data) {
           			obj = JSON.parse(data);
           			if (obj.result == true) { 
           			    channelToken = obj.token;
           			    notificationChannelOpen();
           			} else {
           			    showAlert("Could not request notification channel.  Cannot receive notifications.");
           			}
           		},
           		error: function(xhr, textStatus, error){
           		    showAlert("Error connecting to notification channel: " + textStatus);       
                },
           	}); 
        } catch (err) {
            alert("2" + err.message);            
        }
        
       	$.ajax();        
    }    
}


function makeNotificationMenuClickable() {
    $('.notificationMenuItem').click( function() {
        window.location.href=$(this).data('refpoint');        
    });
    
    $('#notificationMenuHeader').click(function () {
        window.location.href=userURL;                
    });
}

var channelErrors = 0; 

$(document).ready(function() {  
        makeNotificationMenuClickable(); 
        notificationChannelOpen();           
});

