/**
 *@desc: use this program for creating sql file used to creating the database table
 *       according to the fmt string applied to the python struct.unpack() codes.
 */
(function () {
  var originString = 'Lb4sllh4sllllbbbbblbbl4sb4sl4sl4sl4slll4slll4sllllcbbl4sblb4sllbbbbbbbbll4sbbbbbbbb6s4s4sbl4sbll4slbbbbbb4sbbll1s4s4s1sb1sbbbbbbbb1s1s1s1sllll1sllll1sbbh4sllll1s1s1s1s1s1s1s1s1s1scl4sl4s20s30s1s1s1s1s1s1sl1shb4s4s4s4s4s4s4s4s4s4s4s4s4s4s4s4s4s4s4s4sb4s4s4s4s4s4s4s4s4s4sbb1s1s2sbbb2s1s1s1s1s2s2s2shhbbbbbbh2sbllllhllhc4s4sl4sbbbbccbl4s2s2sbbbbbcb1s'
  var i = 0;
  var sum = 0;
  var flag = ['g', 'atp', 'ats', 'opg', 'io', 'zc', 'pf', 'tms', 'debug'];
  var count = [10, 50, 50, 19, 11, 6, 41, 27, 32];

  function genPrefix() {
    if (i <= count[0]) {
      return flag[0] + i.toString();
    } else {
      /*add an blank line, '\n' will lead to 2 blank line */
      console.log('');
      i = 1;
      count.shift();
      flag.shift();
      return flag[0] + i.toString();
    }
  }
  /*start*/
  console.log('drop table train;\n')
  console.log('create table train(')
  
  function handleMatch(str, m1, offset) {
    i++;
    sum++;
    switch (str) {
      /*Unsigned Long 4*/
      case 'L':
        console.log(genPrefix() + ' INT UNSIGNED,')
        break;
      /*long 4*/
      case 'l':
        console.log(genPrefix() + ' INT,');
        break;
      /*short int 2*/
      case 'h':
        console.log(genPrefix() + ' SMALLINT,')
        break;
      /*signed char 1*/
      case 'b':
        console.log(genPrefix() + ' TINYINT,')
        break;
      /*char*/
      case 'c':
        console.log(genPrefix() + ' CHAR(2),')
        break;
      /*char(2)*/
      case '1s':
      case '2s':
      case '4s':
      case '6s':
      case '20s':
      case '30s':
        _i = str.slice(0, -1)
        console.log(genPrefix() + ' CHAR(' + _i * 2 + '),')
        break;
      default :
        console.log('!! Warning !! >>>>' + str + '<<<< is not handled!')
    }
  }

  originString.replace(/(\d{0,2}\w)/g, handleMatch);
  
  console.log(')CHARSET=utf8;')
  
  console.log('=================finish==================')
  console.log('processed data：' + sum);

})();
