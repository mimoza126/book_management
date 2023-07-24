function calculateDaysBetweenDates(begin, end) {
  var beginDate = new Date(begin);
  var endDate = new Date(end);
  var millisecondsPerDay = 1000 * 60 * 60 * 24;
  var millisBetween = endDate.getTime() - beginDate.getTime();
  var days = millisBetween / millisecondsPerDay;
  return Math.floor(days);
}


// 素数を計算するアプリ
// Path: 最終課題\sample.js
function isPrimeNumber(number) {
  if (number < 2) {
    return false;
  }
  for (var i = 2; i < number; i++) {
    if (number % i === 0) {
      return false;
    }
  }
  return true;
}
