function user1handler(options, event, context, callback) {
    if (event.message == 1) {
      options.next_state = 'bot3';
    } 
    callback(options, event, context);
  }
function user2handler(options, event, context, callback) {
    let r1
    if (r1 = /^[0-9]{10}$/.test(event.message)){
      console.log("bot3")
      options.next_state = 'bot4';
    }
    else{
      options.next_state = 'bot3'
      context.sendResponse("Enter a valid 10 digit phone number")
    }
      callback(options, event, context);
    }

  function user3handler(options, event, context, callback) {
      if(r2 = /^[0-9]{12}$/.test(event.message)){
        options.next_state = 'bot5';
      }
      else{
        options.next_state='bot4'
        context.sendResponse("Enter a valid 12 digit number")
      }
        callback(options, event, context);
      }

function user4handler(options, event, context, callback) {
        let date = new Date();
        var month = date.getMonth()+1;
        var day = date.getDate();
        var year = date.getFullYear();
        var currdate = (day+'/'+month+'/'+year);
        let mydate = event.message;
        
        if( r3 = /^(0[1-9]|1[0-9]|2[0-9]|3[0-1])\/(0[1-9]|1[0-2])\/(19|20)\d{2}$/.test(event.message)){
          if( currdate >= mydate)
          {
            options.next_state = 'bot6';
          }
          else{
            context.sendResponse("Enter a valid date")
            options.next_state = 'bot5'
          }
        }
        else{
          options.next_state = 'bot5'
          context.sendResponse("Enter the date in the described format")
        }
          callback(options, event, context);
        }

function user5handler(options, event, context, callback) {
        options.next_state = 'bot7';
        callback(options, event, context);
        }

function user8handler(options, event, context, callback) {
            if (event.message == 1) {
              options.next_state = 'bot8_a';
            } 
            callback(options, event, context);
          }

function user8_2handler(options, event, context, callback) {
            if (event.message == 2) {
              options.next_state = 'bot8_b';
            } 
            callback(options, event, context);
          }

function user8_3handler(options, event, context, callback) {
            if (event.message == 3) {
              options.next_state = 'bot8_c';
            } 
            callback(options, event, context);
          }

function user8_4handler(options, event, context, callback) {
            if (event.message == 4) {
              options.next_state = 'bot8_d';
            } 
            callback(options, event, context);
          }

function user8_5handler(options, event, context, callback) {
            if (event.message == 5) {
              options.next_state = 'bot8_e';
            } 
            callback(options, event, context);
          }

function user8_ahandler(options, event, context, callback) {
            if (event.message == 1 ) {
              options.next_state.gallery = 'bot9';
            } 
            else if (event.message == 2 ) {
              options.next_state.gallery = 'bot9';
            } 
            callback(options, event, context);
          }

function user8_bhandler(options, event, context, callback) { 
            if (r6 = /^((ftp|http|https):\/\/)?www\.([A-z]+)\.([A-z]{2,})/.test(event.message)){
              options.next_state.gallery = 'bot9';
            }
            else{
              options.next_state = 'bot8_b';
              context.sendResponse("Enter a valid URL")
            }
          callback(options, event, context);
        }

function user8_chandler(options, event, context, callback) {
            if (r5 = /^[0-9]{10}$/.test(event.message)){
              options.next_state.gallery = 'bot9';
            }
            else{
              context.sendResponse("Enter a valid 10 digit phone number")
              options.next_state = 'bot8_c';
            }
          callback(options, event, context);
        }

function user8_dhandler(options, event, context, callback) {
          options.next_state.gallery = 'bot9';
        callback(options, event, context);
      }

function user8_ehandler(options, event, context, callback) { 
        options.next_state.gallery = 'bot9';
      callback(options, event, context);
    }

function user9handler(options, event, context, callback) {  
      options.next_state = 'bot10';
    callback(options, event, context);
  }

function user10handler(options, event, context, callback) {     
    options.next_state = 'bot11';
  callback(options, event, context);
}

function user11handler(options, event, context, callback) {
  if(event.messageobj.type == "image"){
    options.next_state = 'bot12';
  }
  else{
    context.sendResponse("Share an image")
    options.next_state = 'bot11'
  }
callback(options, event, context);
}

function user12handler(options, event, context, callback) {     
  options.next_state = 'bot13';
callback(options, event, context);
}

  module.exports.main = {
    user1: user1handler,
    user2: user2handler,
    user3: user3handler,
    user4: user4handler,
    user5: user5handler,
    user8: user8handler,
    user8_2:user8_2handler,
    user8_3:user8_3handler,
    user8_4:user8_4handler,
    user8_5:user8_5handler,
    user8_a:user8_ahandler,
    user8_b:user8_bhandler,
    user8_c:user8_chandler,
    user8_d:user8_dhandler,
    user8_e:user8_ehandler

  }
    module.exports.gallery = {  
    user9: user9handler,
    user10:user10handler,
    user11:user11handler,
    user12:user12handler
  }

 
  