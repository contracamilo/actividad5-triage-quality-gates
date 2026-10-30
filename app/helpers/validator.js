const rules = require('../helpers/validationrules'),
    validate = require('validate.js');

// D-002: las fechas deben ser válidas y checkout posterior a checkin.
const validateDates = function(bookingdates){
  if(!bookingdates || !bookingdates.checkin || !bookingdates.checkout){
    return null;
  }

  const checkin = new Date(bookingdates.checkin),
      checkout = new Date(bookingdates.checkout);

  if(isNaN(checkin.getTime()) || isNaN(checkout.getTime())){
    return {bookingdates: ['Bookingdates must be valid dates']};
  }

  if(checkout <= checkin){
    return {bookingdates: ['Checkout must be after checkin']};
  }

  return null;
};

exports.scrubAndValidate = function(payload, callback){
  if(payload.firstname){
      payload.firstname = payload.firstname.trim();
  }

  if(payload.lastname){
      payload.lastname = payload.lastname.trim();
  }

  callback(payload, validate(payload, rules.returnRuleSet()) || validateDates(payload.bookingdates))
};
