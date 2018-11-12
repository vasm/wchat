var pollInterval = 5000;
var contactsPollInterval = 60000;
var inputField;
var csrftoken;

function scrollToHistoryEnd() {
    $("#chat-history").animate({scrollTop: $("#message-list").height()}, 'slow')
}

$(document).ready(function () {
    // Handler for .ready() called.
    scrollToHistoryEnd();
    $('document, body').animate({
        scrollTop: $('#message-to-send').offset().top 
    }, 'slow');
});


function htmlDecode(encodedStr) {
    return $("<div/>").html(encodedStr).text();
}

function pasteNewMessages(jqXHR) {
    $('#message-list').append(htmlDecode(jqXHR['messages_html']));
}

function pollComplete(jqXHR, textStatus) {
    if (jqXHR['status'] == 'ok') {
        newLastMessage = parseInt(jqXHR['last_message']);
        $('#message-list').append(htmlDecode(jqXHR['messages_html']));
        if (newLastMessage != lastMessage)
            scrollToHistoryEnd();
        lastMessage = newLastMessage;
    } else {
        console.log('Something went wrong when polling messages: ' + jqXHR['error']);
    }
}

function ajaxError(jqXHR, textStatus, errorThrown) {
    console.log("AJAX error:");
    console.log(jqXHR);
}

function pollMessages() {
    $.ajax('/api/messages_from/' + lastMessage + '/', {
        success: pollComplete,
        error: ajaxError,
        complete: function () {
           window.setTimeout(pollMessages, pollInterval);
        } 
    });
}

function sendMessageComplete(jqXHR, textStatus) {
    inputField.val('');
    lastMessage = parseInt(jqXHR['last_message']);
    $('#message-list').append(htmlDecode(jqXHR['message_list_html']));
    scrollToHistoryEnd();
}

function unlockMessageInput() {
    inputField.prop("disabled", false);
}

function sendMessage() {
    console.log('sdfsdf');
    if (inputField.val().length > 0) {
        $.ajax('/api/send/', 
        {
            method: 'POST',
            data: {
                message: inputField.val(),
                last_message: lastMessage,
                //csrftoken: $.cookie('csrftoken')
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: sendMessageComplete,
            error: ajaxError,
            complete: unlockMessageInput
        });
    }
}


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function updateContacts() {
    $.ajax('/api/contacts/', {
        success: function (jqXHR, textStatus) {
            $('#contacts-list').html(htmlDecode(jqXHR['contact_list_html']));
        },
        error: ajaxError,
        complete: function () {
           window.setTimeout(updateContacts, contactsPollInterval);
        } 
    });
}


$(document).ready(function () {
    inputField = $('#message-to-send');

    inputField.keydown(function(event) {
        if (event.keyCode == 13) {
            sendMessage();
            return false;
        } else {
            return true;
        }
    });

    window.setTimeout(pollMessages, pollInterval);
    window.setTimeout(updateContacts, contactsPollInterval);
    $('#send-message').click(sendMessage);
    csrftoken = getCookie('csrftoken');
})