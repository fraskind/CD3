import csv

def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile):
   # template 
   # Start building the HTML structure
   html_content = f'''<!DOCTYPE html>
   <html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <!-- Get your own FontAwesome ID -->
       <script src="https://kit.fontawesome.com/179fb93166.js" crossorigin="anonymous"></script>


      <link rel = "stylesheet" href = "../css/reset.css">
      <link rel = "stylesheet" href = "../css/style.css">
      

      <title>{data["name"]}</title>
   </head>
   <body>
   <a href = "#main">Skip to Main Content</a>
   <nav>
     <ul>
        <li><a href="../index.html">Home Page</a></li>
        <li><a href="../mens.html">Men's Team</a></li>
        <li><a href="../womens.html">Women's Team</a></li>
     </ul>
   </nav>
   <div class="toggle-container">
      <button onclick="toggleDarkMode()">Dark Mode</button>
      <button onclick="toggleHighContrastMode()">High Contrast</button>
   </div>
   <div class="sticky-name">
      <h1>{data["name"]}</h1>
   </div>
   <header>
      <!--Athlete would input headshot-->
      <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200"> 
   </header>
   <main id = "main">
      <section id= "athlete-sr-table">
      <div class="table-container">
         <h2>Athlete's Seasonal Records (SR) per Year</h2>
            <table class="fade-in">
                  <thead>
                     <tr>
                        <th> Year </th>
                        <th> Season Record (SR)</th>
                     </tr>
                  </thead>
                  <tbody>
                  '''
   
   for sr in data["season_records"]:
      sr_row = f'''
                     <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                     </tr>                  
               '''
      html_content += sr_row

   html_content += '''                   
                </tbody>
                  </table>
                  </div>
                     </section>

                        <h2>Race Results</h2>
                        <!-- Floating Action Button above the table -->
                        <section id="athlete-result-table">
                        <div class="table-container">
                           <table id="athlete-table" class="fade-in">
                              <thead>
                                 <tr>
                                    <th>Race</th>
                                    <th>Athlete Time</th>
                                    <th>Athlete Place</th>
                                    <th>Race Comments</th>
                                 </tr>
                              </thead>

                              <tbody>
                  '''

   # add each race as a row into the race table 
   for race in data["race_results"]:
      race_row = f'''
                                 <tr class="result-row">
                                    <td>
                                       <a href="{race["url"]}">{race["meet"]}</a>
                                    </td>
                                    <td>{race["time"]}</td>
                                    <td>{race["finish"]}</td>
                                     <td>{race["comments"]}</td>
                                 </tr>
      '''
      html_content += race_row

   html_content += '''
                              </tbody>

                        </table>
                        </div>
                     </section>
                     </main>
                        <script>
                           document.addEventListener("DOMContentLoaded", function () {
                           const fadeInElements = document.querySelectorAll('.fade-in');

                           function checkVisibility() {
                              fadeInElements.forEach((element) => {
                                    const rect = element.getBoundingClientRect();
                                    if (rect.top <= window.innerHeight && rect.bottom >= 0) {
                                       element.classList.add('visible');
                                    }
                              });
                           }

                              // Check visibility on scroll and on initial load
                              window.addEventListener("scroll", checkVisibility);
                              checkVisibility();
                           });

                           function toggleDarkMode() {
                                 document.body.classList.toggle("dark-mode");
                           }

                           function toggleHighContrastMode() {
                                 document.body.classList.toggle("high-contrast-mode");
                           }
                           // Add the image error handling script
                           document.querySelectorAll('img').forEach(img => {
                              img.onerror = function() {
                                 
                                 this.onerror = null; // Prevents infinite loop if default image missing
                                 this.src = '../images/default_image.jpg';
                                 this.alt = ""
                                 console.log("image is "+this.src)
                              };
                           });
                        </script>
                     <footer>
                     <p>
                     Skyline High School<br>
                     <address>
                     2552 North Maple Road<br>
                     Ann Arbor, MI 48103<br><br>

                     <a href = "https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                    Follow us on Instagram <a href = "https://www.instagram.com/a2skylinexc/" aria-label="Follow us on Instagram"><i class="fa-brands fa-instagram" aria-label="Instagram"></i>  </a> 


                     </footer>
               </body>
         </html>
   '''

   with open(outfile, 'w') as output:
      output.write(html_content)


def main():

   import os
   import glob

   # Define the folder path
   folder_path = 'mens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("mens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "mens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")


   # Define the folder path
   folder_path = 'womens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("womens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "womens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")

if __name__ == '__main__':
    main()
