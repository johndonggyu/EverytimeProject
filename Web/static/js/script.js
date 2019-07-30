$(document).ready(function () {
   var opt = location.href.split('/')[3];
   
   if(opt == "blog"){
      var blog_id = location.href.split('/')[4];
      $.ajax({url: '/word_cloud/'+blog_id, success: function (data) {
        var words_data = $.parseJSON(data);
        
        $('#word_cloud').jQCloud(words_data, {
           shape : 'elliptic', //rectangular
           autoResize : true,
           center : {x:0.5,y:0.5},
           width: 500,
           height: 500,
           //colors: ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976", "#ffeda0", "#ffffcc"],
           fontSize: {
             from: 0.2,
             to: 0.04
           },
        });
  	 }});
   }
   else if(opt == "individual"){
      var major_id = location.href.split('/')[4];
      var pf_id = location.href.split('/')[5];
      $.ajax({url: '/word_cloud/'+major_id+"/"+pf_id, success: function (data) {
        var words_data = $.parseJSON(data);
        
        $('#word_cloud').jQCloud(words_data, {
           shape : 'elliptic', //rectangular
           autoResize : true,
           center : {x:0.5,y:0.5},
           width: 500,
           height: 500,
           //colors: ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976", "#ffeda0", "#ffffcc"],
           fontSize: {
             from: 0.2,
             to: 0.04
           },
        });
  	 }});
   }
   else if(opt == "major"){
   	var major_id = location.href.split('/')[4];
   	$.ajax({url: '/word_cloud/m/'+major_id, success: function (data) {
        var words_data = $.parseJSON(data);
        
        $('#word_cloud').jQCloud(words_data, {
           shape : 'elliptic', //rectangular
           autoResize : true,
           center : {x:0.5,y:0.5},
           width: 500,
           height: 500,
           //colors: ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976", "#ffeda0", "#ffffcc"],
           fontSize: {
             from: 0.2,
             to: 0.04
           },
        });
  	 }});
   	$.ajax({url: '/word_cloud/mn/'+major_id, success: function (data) {
        var words_data = $.parseJSON(data);
        
        $('#n_word_cloud').jQCloud(words_data, {
           shape : 'elliptic', //rectangular
           autoResize : true,
           center : {x:0.5,y:0.5},
           width: 500,
           height: 500,
           //colors: ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976", "#ffeda0", "#ffffcc"],
           fontSize: {
             from: 0.2,
             to: 0.04
           },
        });
  	 }});
   }
   
   
});
