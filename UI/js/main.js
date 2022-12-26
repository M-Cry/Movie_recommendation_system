async function record_movie(elm){
    movie_data = document.getElementById(elm).innerText
    if (movie_data == ""){
        swal({
            title: "OPS!",
            text: "You can't watch an empty movie",
            icon: "error",
            button: "OK Sorry!",
          })
        return 
    }

    let data = await eel.movie_watched(movie_data)(); // Pass data to localhost
    swal("(" + data[1] + ") movie", data[0]+" has been watched", "success");
}

async function update_ui(signal, is_content_based){
    try {
        
        var start_index = 1
        var images = "Collabrative_image_" 
        if(is_content_based === true) {
            // start at the 10th image for content based filtering, otherwise from 0
            start_index = 10
            images = "ContentBased_image_" 
        }

        var mov_counter = 0

        for (let current_movie_index = 0; current_movie_index < signal.length; current_movie_index++) {
            const elm = signal[current_movie_index];
            
            for (let ii = 0; ii < elm.length; ii++) {
                const movies_info_txt_tag = document.getElementById("movie_info_txt_"+(start_index+mov_counter))
                // Iteration of all movies by each genre
                let movies_info = elm[ii][0]
                let poster_link = elm[ii][1]
                
                let movie_genre = movies_info[1]
                let movie_rating = movies_info[3]
                let movie_date = movies_info[movies_info.length - 1]
                
                // UI info update
                let movie_txt = "Genre: "+movie_genre+"<br>Year: "+movie_date+"<br>Rate: "+movie_rating
                movies_info_txt_tag.innerHTML = movie_txt
                document.getElementById(images + (mov_counter)).style.backgroundImage = "url("+poster_link+")"
                
                // i.e. Zookeeper,Comedy,14,42,80,2011
                let movie_specs = movies_info[0]+","+movies_info[1]+","+movies_info[2]+","+movies_info[3]+","+movies_info[4]+","+movies_info[5]
                document.getElementById("movie_info_"+(mov_counter + start_index)).innerText = movie_specs
                
                mov_counter++
            }
        }
        swal("ALGORITHM WORKED SUCCESSFULLY", "recommendations generated", "success");
    } catch (error) {
        swal("ALGORITHM DIDN'T WORK", "Read console for info", "error");
        console.log(error)
    }
}

async function run_collabrative_filter_algo() {
    let signal = await eel.run_collabrative_filter_algo()();
    if (signal == null){
        swal("Ops!", "Python returned none", "error");
        return
    }
    update_ui(signal, false)
}

async function run_content_filter_algo() {
    signal = await eel.run_content_filter_algo()();
    if (signal == null){
        swal("NO RECORDS", "Make sure to watch movies first", "error");
    }else{
        update_ui(signal, true)
    }
}

async function get_graph() {
    signal = await eel.get_graph()();
    if (signal[0] == null){
        // if history is null and calling from content based algo.
        swal("NO DATA PROVIDED", "Make sure to Run Algo. first", "error");
    }
}

async function get_statistics() {
    await eel.get_statistics()();
}