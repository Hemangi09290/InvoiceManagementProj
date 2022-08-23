$(document).ready(function(){

$("#id_date").attr('readonly','readonly');	
$("#id_billable_task").attr('placeholder', 'Write Billable Task');
$("#id_nonbillable_task").attr('placeholder', 'Write Non Billable Task');
$("#id_date").attr('placeholder', 'mm/dd/yyyy');
$("#id_billable_hours").attr('placeholder', 'h:m');
$("#id_nonbillable_hours").attr('placeholder', 'h:m');

  $('#submit').click(function(e) {
  	clear();
  if(condition()){
       e.preventDefault();
    }
  else{
  	$('#entry').submit();
  }
});
});
function condition()
{
var project_id = document.entry.id_project_id;
var billable_task = document.entry.id_billable_task;
var nonbillable_task = document.entry.id_nonbillable_task;
var date = document.entry.date;
var billable_hours = document.entry.id_billable_hours;
var nonbillable_hours = document.entry.id_nonbillable_hours;
if(projectselect(project_id))
{
if(hoursvalid(billable_hours,"Billable ","billable_hourserror"))
{
if(Taskvalid(billable_task,"Billable ","billable_taskerror"))
{
if(dateempty(date))
{
	if(datevalid(date))
	{
		if(hoursvalid(nonbillable_hours,"Non Billable ","nonbillable_hourserror"))
          {
          	if(Taskvalid(nonbillable_task,"Non Billable ","nonbillable_taskerror"))
               {
               		return false
               }
          }
	}
}
}
}
}
return true
}
function projectselect(project_id)
{
if(project_id.value == "")
{
document.getElementById("projecterror").innerHTML="Select your Project name !";
project_id.focus();
return false;
}
return true;
}
function hoursvalid(hours,msg,error_elem)
{
var hours_val = hours.value;
if (hours_val == 0 )
{
document.getElementById(error_elem).innerHTML=msg+"Hours should not be empty !";
hours.focus();
return false;
}
return true;
}
function Taskvalid(task,msg,error_elem)
{
	var Task_len = task.value;
	if(Task_len==0)
	{
		document.getElementById(error_elem).innerHTML=msg+"Task should not be empty !";
		task.focus();
		return false;

	}
	return true;
}
function dateempty(date)
{
	var date_val = date.value;
	if(date_val==0)
	{
		document.getElementById("dateerror").innerHTML="Date should not be empty !";
		date.focus();
		return false;

	}
	return true;
}
function datevalid(e_date)
{
var text = e_date.value;
var comp = text.split('/');
var m = parseInt(comp[0], 10);
var d = parseInt(comp[1], 10);
var y = parseInt(comp[2], 10);
var date = new Date(y,m-1,d);
if (date.getFullYear() == y && date.getMonth() + 1 == m && date.getDate() == d) {
  return true;
} else {
	  document.getElementById("dateerror").innerHTML="Date should be valid !";
	  return false;
}
}
function clear()
{
	document.getElementById("dateerror").innerHTML=""
	document.getElementById("nonbillable_taskerror").innerHTML=""
	document.getElementById("billable_hourserror").innerHTML=""
	document.getElementById("billable_taskerror").innerHTML=""
	document.getElementById("nonbillable_hourserror").innerHTML=""
	document.getElementById("projecterror").innerHTML=""
}