<?php  

if(isset($_POST["id"]))  //Abfrage für Info von Landkreisen. Wenn ein Landkreis angeklickt wird.
 {  
      $output = '';  
      $connect = mysqli_connect("Server", "xxx", "xxx", "xxx");  
      $query = "SELECT * FROM covid_p WHERE id = '".$_POST["id"]."'";  
      $query2 = "SELECT * FROM covid_p WHERE land LIKE (SELECT land FROM covid_p WHERE id = '".$_POST["id"]."')"; 

      $result = mysqli_query($connect, $query);  
      $result2 = mysqli_query($connect, $query2); 
      $output .= '  
      <div class="table-responsive">  
      
           <table class="table table-bordered">';  

          // Anzahl der Bevölkerung wird für jeden Landkreis in einem bestimmten Bundesland in der Tabelle in einer unsichtbaren Form gespeichert.
          // Diese werden dann entnommen, womit die Graf geplotet wird.
           while($ro = mysqli_fetch_array($result2))
           {
               $output .= '  
               <tr> 
                    <td width="70%" class="bundesland" value='.$ro["land"].' id='.$ro["bevoelkerung"].' style="display:none;">'.$ro["landkreisName"].'</td>  
                    <td width="70%" class="Fallzahlen" id='.$ro["item0"].' style="display:none;">'.$ro["item0"].'</td>  
                    <td width="70%" class="Fallzahlen" id='.$ro["item1"].' style="display:none;">'.$ro["item1"].'</td>
                    <td width="70%" class="Fallzahlen" id='.$ro["item2"].' style="display:none;">'.$ro["item2"].'</td>
                    <td width="70%" class="Fallzahlen" id='.$ro["item3"].' style="display:none;">'.$ro["item3"].'</td>
                    <td width="70%" class="Fallzahlen" id='.$ro["item4"].' style="display:none;">'.$ro["item4"].'</td>
                    <td width="70%" class="Fallzahlen" id='.$ro["item5"].' style="display:none;">'.$ro["item5"].'</td>
                    <td width="70%" class="Fallzahlen" id='.$ro["item6"].' style="display:none;">'.$ro["item6"].'</td>
                    <td width="70%" class="Fallzahlen" id='.$ro["item7"].' style="display:none;">'.$ro["item7"].'</td>
               </tr>';          
           } 

     // Die Daten des angeklickten Landkreis werden in einer Tabelle Teilweise in einer unsichtbaren Form gespeichert.
     // Diese werden dann entnommen, womit die Graf geplotet wird.
      while($row = mysqli_fetch_array($result))  
      {  
           $output .= '  
               <tr>  
                    <td width="30%"><label>Kreis</label></td>  
                    <td width="70%" id="landkreisname">'.$row["landkreisName"].'</td>  
               </tr>
                <tr>  
                     <td width="30%"><label>Bevölkerung</label></td>  
                     <td width="70%">'.$row["bevoelkerung"].'</td>  
                </tr>  
                <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz aktuel</label></td>  
                    <td width="70%" id="0" style="display:none;">'.$row["item0"].' </td>  
                </tr>                
                <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 1</label></td>  
                    <td width="70%" id="1" style="display:none;">'.$row["item1"].' </td>  
                </tr>
                <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 2</label></td>  
                    <td width="70%" id="2" style="display:none;">'.$row["item2"].'</td>  
               </tr>  
               <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 3</label></td>  
                    <td width="70%" id="3" style="display:none;">'.$row["item3"].'</td>  
               </tr>  
               <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 4</label></td>  
                    <td width="70%" id="4" style="display:none;">'.$row["item4"].'</td>  
               </tr>  
               <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 5</label></td>  
                    <td width="70%" id="5" style="display:none;">'.$row["item5"].' </td>  
               </tr>  
               <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 6</label></td>  
                    <td width="70%" id="6" style="display:none;">'.$row["item6"].'</td>  
               </tr>  
               <tr>  
                    <td width="30%" style="display:none;"><label>7TageInzidenz Tag 7</label></td>  
                    <td width="70%" id="7" style="display:none;">'.$row["item7"].' </td>  
               </tr>


                ';  
      }  

      //$output .= "</table></div>";  
      //while($row1 = mysqli_fetch_array($result2))  
      //{  
       //$output .= "<input type='hidden' id='".$row1["id"]."' name='".$row1["landkreisName"]."' value='".$row1["item0"].",".$row1["item1"].",".$row1["item2"].",".$row1["item3"].",".$row1["item4"].",".$row1["item5"].",".$row1["item6"].",".$row1["item6"]."'>";
      //}


      echo $output;  
 }  
 if(isset($_POST["land"]))  //Abfrage für Landkreis-Bundesland-zugehörigkeit
 {  
      $output = '';  
      $connect = mysqli_connect("n1nlmysql29plsk.secureserver.net:3306", "covid_", "covid_19", "covid_");  
      $query = "SELECT * FROM covid_p WHERE land LIKE '".$_POST["land"]."'";
      $result1 = mysqli_query($connect, $query);  

      $output1 .= '<option value="" class="view_data" disabled selected> Wählen Sie ein Landkreis</option>';
      while($row1 = mysqli_fetch_array($result1))  
      {  
           $output1 .= "<option value='".$row1["id"]."' class='view_data'>".$row1["landkreisName"]."</option>";
           
      }  
      echo $output1;  
 }
 ?>

