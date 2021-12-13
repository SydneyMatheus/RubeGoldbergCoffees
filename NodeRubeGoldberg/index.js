//import firebase from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js"
//import {getDatabase, query, ref, onValue} from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-database.js'
const express = require ("express")
const cors = require ("cors")
const firebase = require ("firebase/app")
const {getDatabase, query, ref, onValue, limitToLast, get, child } = require ('firebase/database')

const port = 5000

const app = express()
app.use(cors())

var gCafeStatus = false
var gTemperature

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Request-With, Content-Type, Accept");
    next();
});

const firebaseApp = firebase.initializeApp ({
    apiKey: "AIzaSyDCNjoSmXJasSthJPlIiHoQ9dQjA8fJAck",  
    authDomain: "rubegoldberginths.firebaseapp.com",
    databaseURL: "https://rubegoldberginths-default-rtdb.firebaseio.com",
    projectId: "rubegoldberginths",
    storageBucket: "rubegoldberginths.appspot.com",
    messagingSenderId: "896241581822",
    appId: "1:896241581822:web:5bb3659d75acb3b85cafaf",
    measurementId: "G-XK9H6Z4XVN"
}, 'firebaseApp');

//var db = getDatabase (firebaseApp);
const dbRef = ref(getDatabase(firebaseApp));

app.listen(port, ()=> {})

app.use(express.static(__dirname+"/template/static/"))

app.get('/getData', (req, res)=> {
    get(child(dbRef, 'status/rubeGoldberg/')).then((snapshot) => {
        if (snapshot.exists()) {

          console.log(snapshot.val());
          if (snapshot.val())
          {
            get(child(dbRef, 'status/coffe/')).then((snapshot) => {
              if (snapshot.exists()) {
                if (snapshot.val()){
                
                get(child(dbRef, 'status/temperatura/')).then((snapshot) => {
                  if (snapshot.exists()) {
                      res.send({'temperature' : snapshot.val().temp, 'status' :"Seu café está pronto!", 'flag': true})
                      console.log(snapshot.val());
                  } else {
                    console.log("No data available");
                  }
                }).catch((error) => {
                  console.error(error);
                });

              }  else {
                res.send({"flag": false});
              }
              } else {
                console.log("No data available");
              }
            }).catch((error) => {
              console.error(error);
            });

            /*get(child(dbRef, 'status/temperatura/')).then((snapshot) => {
                if (snapshot.exists()) {
                    res.send({'temperature' : snapshot.val().temp, 'status' :"Seu café está pronto!", 'flag': true})
                    console.log(snapshot.val());
                } else {
                  console.log("No data available");
                }
              }).catch((error) => {
                console.error(error);
              });*/

              /*if ((gTemperature > highTemp) || (highTemp == undefined))
              {
                  highTemp = gTemperature
              }
              if ((gTemperature < lowTemp) || (lowTemp == undefined))
              {
                  lowTemp = gTemperature
              }*/
              //res.send({'temperature' : snapshot.val()})
          } else {
              res.send({"flag": false});
          }
        } else {
          console.log("No data available");
        }
      }).catch((error) => {
        console.error(error);
      });


})

//app.get('/getTemp', (req, res)=> {
//    get(child(dbRef, 'status/temperatura/')).then((snapshot) => {
//        if (snapshot.exists()) {

//          console.log(snapshot.val());
//          if (gCafeStatus)
 //         {
              /*if ((gTemperature > highTemp) || (highTemp == undefined))
              {
                  highTemp = gTemperature
              }
              if ((gTemperature < lowTemp) || (lowTemp == undefined))
              {
                  lowTemp = gTemperature
              }*/
 //             res.send({'temperature' : snapshot.val()})
 //         }


 //       } else {
  //        console.log("No data available");
  //      }
 //     }).catch((error) => {
//console.error(error);
  //    });


//})

app.get('/getCafeStatus', (req, res)=> {
    if (gCafeStatus)
        res.send({'status' :"Seu café está pronto!"})
})



/*onValue(query(ref(db, 'status/coffe/')),(snapshot) => {
    const data = snapshot.val();
    gCafeStatus = data;
    console.log("Café Status: ", gCafeStatus);
});

const temp = query(ref(db, 'status/temperatura/'), limitToLast(1));
onValue(temp, (snapshot) => {
  const data = snapshot.val();
  gTemperature = Object.values(data);
  console.log("temperatura: ", gTemperature);
});*/