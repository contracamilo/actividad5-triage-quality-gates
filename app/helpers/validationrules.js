exports.returnRuleSet = function(){
  const constraints = {
    firstname: {presence: true},
    lastname: {presence: true},
    // D-003: totalprice debe ser numérico y no negativo (antes solo se exigía presencia).
    totalprice: {presence: true, numericality: {greaterThanOrEqualTo: 0}},
    depositpaid: {presence: true},
    'bookingdates.checkin': {presence: true},
    'bookingdates.checkout': {presence: true},
  };

  return constraints
}
