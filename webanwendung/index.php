
 <!DOCTYPE html>  
<html>  
     <head>  
           <title>COVID-19: Prognosen auf kommunaler Ebene</title>  
           <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>  
           <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />  
           <link rel="stylesheet" href="/css/style.css" />  
           <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>  
           <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
     </head>  
     <body> 

          <br />  
          <!--------------------------------------------------------HEADER--------------------------------------------------------->
          <div class="container" style="background: linear-gradient(to right, rgb(228,   205,   226) 0%, rgb(242, 180,   181) 60% );width:100%;margin-top:-20px;border-bottom:solid 4px #86487c;">
               <div class="container" >
               
                    <div style="float:left"><img src="img/Logo.png" alt="" style="float:right; width:120px; "></div>
                    <div style="width:60%;">
                         <h3 align="left" style="color:#743554; font-size:2em;font-weight:bold">COVID-19-Prognose</h3>  
                         <h3 align="left" style="color:#fff;font-size:1.5em;font-weight:bold">auf kommunaler Ebene in Deutschland</h3>
                    </div>
                    <div style="   float: right; background-color: #4a2b45; 
                                   padding: 3px;">
                             <span style=" "><a href="#" style="color:#fff;text-decoration:none;">HOME</a></span> 
                    </div>

               </div>
          </div>

          <div class="container" >
               <div style="   float: right; background-color: #86487c; 
                                   padding: 3px;">
                    <span style=""><a href="/about.php" style="color:#fff;text-decoration:none;">ÜBER DAS PROJEKT</a></span> 
               </div>
          </div>




          <!-------------------------------------------------Dropdownlist Bundesland----------------------------------------------------->
          <div class="container" style="  margin-top:20px; width:700px">  
               <div class="table-responsive;">  <span class="" style="margin-right:10px;">Bundesland</span>  
                    <select name="" id="BLand" class="form-select"  title="Choose one of the following...">
                         <option value="" class="" disabled selected>
                              Wählen Sie ein Bundesland
                         </option>                         
                         <option value="Schleswig-Holstein" class="">
                              Schleswig-Holstein
                         </option>                              
                         <option value="Hamburg" class="">
                               Hamburg
                         </option>
                         <option value="Niedersachsen" class="">
                              Niedersachsen
                         </option>
                         <option value="Bremen" class="">
                              Bremen                              
                         </option>
                         <option value="Nordrhein-Westfalen" class="">
                         Nordrhein-Westfalen
                         </option>
                         <option value="Hessen" class="">
                              Hessen    
                         </option>                              
                         <option value="Rheinland-Pfalz" class="">
                               Rheinland-Pfalz
                         </option>
                         <option value="Baden-Württemberg" class="">
                          Baden-Württemberg
                         </option>
                         <option value="Bayern" class="">
                              Bayern
                         </option>
                         <option value="Saarland" class="">
                              Saarland
                         </option>
                         <option value="Berlin" class="">
                              Berlin                              
                              </option>
                         <option value="Brandenburg" class="">
                              Brandenburg
                         </option>
                         <option value="Mecklenburg-Vorpommern" class="">
                              Mecklenburg-Vorpommern
                         </option>
                         <option value="Sachsen" class="">
                              Sachsen
                         </option>
                         <option value="Sachsen-Anhalt" class="">
                              Sachsen-Anhalt
                         </option>
                         <option value="Thüringen" class="">
                              Thüringen
                         </option>
                    </select>

                    <!-----------------------------------------------Query für 2. Dropdownlist von Landkreisen------------------------------------------------------->
                    <?php  
                         $connect = mysqli_connect("n1nlmysql29plsk.secureserver.net:3306", "covid_", "covid_19", "covid_");  
                         $query = "SELECT * FROM covid_p";  
                         $result = mysqli_query($connect, $query);  
                    ?>  

                    <div class=".col-md-8" style="margin-top:10px;">
                         <span class=""style="margin-right:24px;">Landkreis</span> 
                         <select name="" id="art" class=""></br> 
                              <option value="" class="" disabled selected>
                                   Wählen Sie einen Landkreis
                              </option> 
                              <!-----------------------------------------------Erzeugen von 2. Dropdownlist------------------------------------------------------->
                              <?php  
                              while($row = mysqli_fetch_array($result))  
                              {  
                              ?>  <option value="<?php echo $row["id"]; ?>" class="view_data">
                                   <?php echo $row["landkreisName"]; ?>
                                   </option>
                              <?php  
                              }  
                              ?>  
                         </select> 
                    </div>
               </div>  

               <!-----------------------------------------------Container für 1. Chart------------------------------------------------------->
               <div id="chartContainer" style="height: 300px; width: 100%; margin-top:20px;">
                    <h4 class="">Pandemiegeschehen im Laufe der Zeit</h4>
                    <div style="border: 1px solid gray;">
                         <img src="/img/verlauf.gif" alt="" style="width:600px;">
                    </div>
               </div>
               <!-----------------------------------------------Container für Landkreise und deren Bewohneranzhal ------------------------------------------------------->
               <div id="dataModal" style="margin:20px;">  </div>
               <!-----------------------------------------------Container für 2. Chart------------------------------------------------------->
               <div id="chartContainer1" style="height:400px;"></div>
          </div>  

          <!-----------------------------------------------Footer------------------------------------------------------->
          <div class="container">
               <div class="" style="position: fixed;  bottom: 0;  width: 80%;opacity: 0.9;
                    background: linear-gradient(to right, rgb(228,   205,   226) 0%,
                    rgb(242, 180,   181) 60% );color: white;padding:10px; height:40px;">

                    <span style="margin-right:20px; margin-left:10px; "><a href="#" style="color:#542726;text-decoration:none;"> HOME </a></span> 
                    <span style=""><a href="/about.php" style="color:#542726;text-decoration:none;"> ÜBER DAS PROJEKT </a></span> 
               </div>
          </div>



          
     </body>  
</html>  

<!-----------------------------------------------JS------------------------------------------------------->

 <script>  
 $(document).ready(function(){  
      $('#art').change(function(){  
           var id = (this.value);  
           //-----------------------------------------------AJAX fürs Aktualisieren der Teile der Webseite-------------------------------------------------------

           $.ajax({  
                url:"select.php",  // Die Ajax-Abfrage wird in "select.php" behandelt.
                method:"post",  
                data:{id:id},  
                success:function(data){ // Wenn AJAX-Anfrage gelungen ist:  
                     $('#dataModal').html(data);  //Ausgabe von Tabele mit Landkreisname und Bevölkerung. Die benötigte Daten werden aus Server in unsichtbaren td-Elementen gespeichert.
                    
                    //-----------------------------------------------7Tageinzidenz-Graph ploten---------------------------------------------------------------                     
                    var today = new Date(); 
                    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();

                    var y = 0;
                    var data = [];
                    var dataSeries = { type: "line" };
                    var dataPoints = [];

                    dataPoints.push({
                    y: parseFloat($('#0').text()), indexLabel: " aktuele Inzidenz", markerColor: "red", markerType: "triangle",
                    label: date
                    });

                    for(var x = 1; x<8 ; x++){//Die zu plotenden Daten (8 Werte) werden aus td-Elementen von Tabelle entnommen.
                         id = "#" + x.toString();
                         dataPoints.push({
                         y: parseFloat($(id).text()),
                         label: today.getDate()+x+'-'+(today.getMonth()+1)+'-'+today.getFullYear()
                         });

                    }

                    dataSeries.dataPoints = dataPoints;
                    data.push(dataSeries);
                    var options = {
                         zoomEnabled: true,
                         animationEnabled: true,
                         title: {
                              text: "7Tageinzidenz in nächsten 7 Tagen in "+$('#landkreisname').text(),
                              fontSize: 25
                         },
                         axisX: {
                              labelAngle: -60
                         },
                         axisY: {
                              includeZero: false
                         },
                         data: data
                    };

                    var chart = new CanvasJS.Chart("chartContainer", options);
                    chart.render();// Chart ploten.
                    

                     


                    //-----------------------------------------------Bevölkerung ploten---------------------------------------------------------------                     
                    var y = 0;
                    var data = [];
                    var dataSeries = { type: "doughnut", indexLabelFontSize: 12 };
                    var dataPoints = [];

                    for(var x = 0; x< $('.bundesland').length ; x++){//Die zu plotenden Daten (Bevölkerung) werden aus td-Elementen von Tabelle entnommen.
                         dataPoints.push({
                         y: parseFloat($('.bundesland')[x].getAttribute('id')),
                         label: $('.bundesland')[x].innerText
                         });
                    }
                    dataSeries.dataPoints = dataPoints;
                    data.push(dataSeries);

                    var options2 = {
                         height:350,
                         zoomEnabled: true,
                         animationEnabled: true,
                         title: {
                              text: "Bevölkerung in Bundesland "+$('.bundesland')['0'].getAttribute('value'),
                              fontSize: 25
                         },                      
                         data: data
                    };
                    var chart = new CanvasJS.Chart("chartContainer1", options2);
                    chart.render();// Chart ploten.
                    }
               });  
          });  

//-----------------------------------------------AJAX für Dropdownlist von Bundesländer---------------------------------------------------------------                     
//Je nach Bundesland werden Landkreisenamen in einem anderen Dropdownlist zur Vefügung gestellt.

      $('#BLand').change(function(){  
           
           var land = (this.value);  
           $('#dataModal').html(""); 
           $.ajax({  
                url:"select.php",  // Die Ajax-Abfrage wird in "select.php" behandelt.
                method:"post",  
                data:{land:land},  
                success:function(data){  
                    $('#art').html(data);  

                }  
           });  
      });  
 });  
 </script>





