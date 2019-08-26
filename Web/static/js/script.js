var from_size = 0.2; //0.2
var to_size = 0.04; //0.04
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
             from: from_size,
             to: to_size
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
             from: from_size,
             to: to_size
           },
        });
  	 }});
      //chartjs
     $.ajax({url: '/chart/'+major_id+"/"+pf_id, success: function (data) {
        var charts_data = $.parseJSON(data);
        //console.log(charts_data);
        var myChart = document.getElementById('myChart1').getContext('2d'); //create our chart

	    // Global options
	    Chart.defaults.global.defaultFontFamily = 'Lato',
	    Chart.defaults.global.defaultFontSize = 18;
	    Chart.defaults.global.defaultFontColor = '#777';

	    var massPopChart = new Chart(myChart, {
	        type:'polarArea', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	        data:{
	            labels:['평점'],
	            datasets:[{
	                label: '수업(개)',
	                data:[
	                charts_data[0].averageScore,
	                ],
	                //backgroundColor: 'green'
	                backgroundColor: [
	                  'rgba(255, 99, 132, 0.6)',
	                  'rgba(54, 162, 235, 0.6)',
	                  'rgba(255, 206, 86, 0.6)',
	                  'rgba(75, 192, 192, 0.6)',
	                ],
	                borderWidth: 4,
	                borderColor: '#777',
	                hoverBorderWidth:3,
	                hoverBorderColor: '#000'
	            }]
	        },
	        options:{
	          maintainAspectRatio: false,
	          title:{
	            display:true,
	            text: decodeURI(pf_id)+' 교수님 평점',
	            fontSize: 25
	          },
	          legend: {
	            display: true,
	            position: 'right',
	            labels: {
	              fontColor: 'rgba(255,99,132)'
	            }
	          }
	        },
	        layout: {
	          padding: {
	            left: 0,
	            right: 0,
	            bottom: 0,
	            top: 0
	          }
	        },
	        tooltips:{
	          enabled: true
	        }

	    });
	    ////////////////////////////////////////
	    var myChart = document.getElementById('myChart2').getContext('2d'); //create our chart

		  // Global options
		  Chart.defaults.global.defaultFontFamily = 'Lato',
		  Chart.defaults.global.defaultFontSize = 18;
		  Chart.defaults.global.defaultFontColor = '#777';

		  var massPopChart = new Chart(myChart, {
		      type:'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		      data:{
		          labels:['많음', '보통', '적음'],
		          datasets:[{
		              label: '수업(개)',
		              data:[
		              charts_data[0].assignmentMany,
		              charts_data[0].assignmentNorm,
		              charts_data[0].assignmentNone,
		              ],
		              //backgroundColor: 'green'
		              backgroundColor: [
		                'rgba(255, 99, 132, 0.6)',
		                'rgba(54, 162, 235, 0.6)',
		                'rgba(255, 206, 86, 0.6)',
		                'rgba(75, 192, 192, 0.6)',
		              ],
		              borderWidth: 4,
		              borderColor: '#777',
		              hoverBorderWidth:3,
		              hoverBorderColor: '#000'
		          }]
		      },
		      options:{
		        maintainAspectRatio: false,
		        title:{
		          display:true,
		          text: decodeURI(pf_id)+' 교수님 과제 비율',
		          fontSize: 25
		        },
		        legend: {
		          display: true,
		          position: 'right',
		          labels: {
		            fontColor: 'rgba(255,99,132)'
		          }
		        }
		      },
		      layout: {
		        padding: {
		          left: 0,
		          right: 0,
		          bottom: 0,
		          top: 0
		        }
		      },
		      tooltips:{
		        enabled: true
		      }

		  });
		////////////////////////////
		var myChart = document.getElementById('myChart3').getContext('2d'); //create our chart

		  // Global options
		  Chart.defaults.global.defaultFontFamily = 'Lato',
		  Chart.defaults.global.defaultFontSize = 18;
		  Chart.defaults.global.defaultFontColor = '#777';

		  var massPopChart = new Chart(myChart, {
		      type:'doughnut', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		      data:{
		          labels:['많음', '보통', '적음'],
		          datasets:[{
		              label: '수업(개)',
		              data:[
		              charts_data[0].team_projectMany,
		              charts_data[0].team_projectNorm,
		              charts_data[0].team_projectNone,
		              ],
		              //backgroundColor: 'green'
		              backgroundColor: [
		                'rgba(255, 99, 132, 0.6)',
		                'rgba(54, 162, 235, 0.6)',
		                'rgba(255, 206, 86, 0.6)',
		                'rgba(75, 192, 192, 0.6)',
		              ],
		              borderWidth: 4,
		              borderColor: '#777',
		              hoverBorderWidth:3,
		              hoverBorderColor: '#000'
		          }]
		      },
		      options:{
		        maintainAspectRatio: false,
		        title:{
		          display:true,
		          text: decodeURI(pf_id)+' 교수님 팀플 비율',
		          fontSize: 25
		        },
		        legend: {
		          display: true,
		          position: 'right',
		          labels: {
		            fontColor: 'rgba(255,99,132)'
		          }
		        }
		      },
		      layout: {
		        padding: {
		          left: 0,
		          right: 0,
		          bottom: 0,
		          top: 0
		        }
		      },
		      tooltips:{
		        enabled: true
		      }

		  })
		////////////////////////////
		var myChart = document.getElementById('myChart4').getContext('2d'); //create our chart

		  // Global options
		  Chart.defaults.global.defaultFontFamily = 'Lato',
		  Chart.defaults.global.defaultFontSize = 18;
		  Chart.defaults.global.defaultFontColor = '#777';

		  var massPopChart = new Chart(myChart, {
		      type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		      data:{
		          labels:['학점느님', '비율 채워줌', '매우 깐깐함', 'F폭격기'],
		          datasets:[{
		              label: '수업(개)',
		              data:[
		              charts_data[0].creditGod,
		              charts_data[0].creditProportion,
		              charts_data[0].creditTough,
		              charts_data[0].creditFbomb,
		              ],
		              //backgroundColor: 'green'
		              backgroundColor: [
		                'rgba(255, 99, 132, 0.6)',
		                'rgba(54, 162, 235, 0.6)',
		                'rgba(255, 206, 86, 0.6)',
		                'rgba(75, 192, 192, 0.6)',
		              ],
		              borderWidth: 4,
		              borderColor: '#777',
		              hoverBorderWidth:3,
		              hoverBorderColor: '#000'
		          }]
		      },
		      options:{
		        maintainAspectRatio: false,
		        title:{
		          display:true,
		          text: decodeURI(pf_id)+' 교수님 학점 비율',
		          fontSize: 25
		        },
		        legend: {
		          display: true,
		          position: 'right',
		          labels: {
		            fontColor: 'rgba(255,99,132)'
		          }
		        }
		      },
		      layout: {
		        padding: {
		          left: 0,
		          right: 0,
		          bottom: 0,
		          top: 0
		        }
		      },
		      tooltips:{
		        enabled: true
		      }

		  })
		////////////////////////////
		var myChart = document.getElementById('myChart5').getContext('2d'); //create our chart

		  // Global options
		  Chart.defaults.global.defaultFontFamily = 'Lato',
		  Chart.defaults.global.defaultFontSize = 18;
		  Chart.defaults.global.defaultFontColor = '#777';

		  var massPopChart = new Chart(myChart, {
		      type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		      data:{
		          labels:['혼용', '직접호명', '지정좌석', '전자출결', '반영안함'],
		          datasets:[{
		              label: '수업(개)',
		              data:[
		              charts_data[0].attendanceMix,
		              charts_data[0].attendanceDirect,
		              charts_data[0].attendanceDesignated,
		              charts_data[0].attendanceElectronic,
		              charts_data[0].attendanceNone,
		              ],
		              //backgroundColor: 'green'
		              backgroundColor: [
		                'rgba(255, 99, 132, 0.6)',
		                'rgba(54, 162, 235, 0.6)',
		                'rgba(255, 206, 86, 0.6)',
		                'rgba(75, 192, 192, 0.6)',
		                'rgba(100, 52, 192, 0.6)',
		              ],
		              borderWidth: 4,
		              borderColor: '#777',
		              hoverBorderWidth:3,
		              hoverBorderColor: '#000'
		          }]
		      },
		      options:{
		        maintainAspectRatio: false,
		        title:{
		          display:true,
		          text: decodeURI(pf_id)+' 교수님 출결 비율',
		          fontSize: 25
		        },
		        legend: {
		          display: true,
		          position: 'right',
		          labels: {
		            fontColor: 'rgba(255,99,132)'
		          }
		        }
		      },
		      layout: {
		        padding: {
		          left: 0,
		          right: 0,
		          bottom: 0,
		          top: 0
		        }
		      },
		      tooltips:{
		        enabled: true
		      }

		  })
		////////////////////////////
		var myChart = document.getElementById('myChart6').getContext('2d'); //create our chart

		  // Global options
		  Chart.defaults.global.defaultFontFamily = 'Lato',
		  Chart.defaults.global.defaultFontSize = 18;
		  Chart.defaults.global.defaultFontColor = '#777';

		  var massPopChart = new Chart(myChart, {
		      type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		      data:{
		          labels:['네번 이상', '세 번', '두 번', '한 번', '없음'],
		          datasets:[{
		              label: '수업(개)',
		              data:[
		              charts_data[0].test4above,
		              charts_data[0].test3,
		              charts_data[0].test2,
		              charts_data[0].test1,
		              charts_data[0].testNone,
		              ],
		              //backgroundColor: 'green'
		              backgroundColor: [
		                'rgba(255, 99, 132, 0.6)',
		                'rgba(54, 162, 235, 0.6)',
		                'rgba(255, 206, 86, 0.6)',
		                'rgba(75, 192, 192, 0.6)',
		                'rgba(100, 52, 192, 0.6)',
		              ],
		              borderWidth: 4,
		              borderColor: '#777',
		              hoverBorderWidth:3,
		              hoverBorderColor: '#000'
		          }]
		      },
		      options:{
		        maintainAspectRatio: false,
		        title:{
		          display:true,
		          text: decodeURI(pf_id)+' 교수님 시험 횟수',
		          fontSize: 25
		        },
		        legend: {
		          display: true,
		          position: 'right',
		          labels: {
		            fontColor: 'rgba(255,99,132)'
		          }
		        }
		      },
		      layout: {
		        padding: {
		          left: 0,
		          right: 0,
		          bottom: 0,
		          top: 0
		        }
		      },
		      tooltips:{
		        enabled: true
		      }

		  })
		////////////////////////////
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
             from: from_size,
             to: to_size
           },
        });
  	 }});
   	$.ajax({url: '/word_cloud/mn/'+major_id, success: function (data) {
        var words_data = $.parseJSON(data);
        if (words_data.length == 0){
        	$('#n_word_cloud')[0].innerHTML = '<img src="/static/img/nodata.png">';
        }
        else{
	        $('#n_word_cloud').jQCloud(words_data, {
	           shape : 'elliptic', //rectangular
	           autoResize : true,
	           center : {x:0.5,y:0.5},
	           width: 500,
	           height: 500,
	           //colors: ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976", "#ffeda0", "#ffffcc"],
	           fontSize: {
	             from: 0.1,
	             to: 0.02
	           },
	        });
    	}
  	 }});
   }
   
   
});
