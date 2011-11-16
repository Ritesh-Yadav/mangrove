//All the deadline related drop-downs. They are very very very annoying.
DW.DeadlineDetails = function(){
    this.deadlineSection = '#frequency_values';
    this.deadlineEnabledControl = 'input[name=deadline_enabled]';
    this.deadlineEnabledCheckedControl = 'input[name=deadline_enabled]:checked';
    this.frequencyPeriodControl = 'select[name=frequency_period]';
    this.deadlineTypeControl = 'select[name=deadline_type]'; //For the control which lets user select Same and Following. I wish i had a better name for this one.
    this.deadlineMonthControl = 'select[name=deadline_month]';
    this.deadlineWeekControl = 'select[name=deadline_week]';
    this.month_block_id = '#month_block';
    this.week_block_id = '#week_block';
    this.reminders_block_id = '#reminders_section';
};

DW.DeadlineDetails.prototype = {
    init: function(){
        var is_deadline_enabled = ($(this.deadlineEnabledCheckedControl).val() === "True");
        if(is_deadline_enabled){
            this.show();
        }else{
            this.hide();
        }
        return true; //It's a Best Practice to return either true or false when there are only side effects happening inside a method.
    },
    hide: function(){
        $(this.deadlineSection).hide();
        $(this.reminders_block_id).hide();
    },
    show: function(){
        var is_week = ($(this.frequencyPeriodControl).val() === "week");
        if(is_week){
            this.toggle_when_week_is_selected();
        }else{
            this.toggle_when_month_is_selected();
        }
        $(this.deadlineSection).show(); //Showing stuff after everything has been set, should make the user not see that we are changing values in browsers like IE6-7
        $(this.reminders_block_id).show();
    },
    disable: function(){

    },
    toggle_when_month_is_selected: function(){
        $(this.month_block_id).show();
        $(this.week_block_id).hide();
    },
    toggle_when_week_is_selected: function(){
        $(this.week_block_id).show();
        $(this.month_block_id).hide();
    }
};

var deadlineDetails = new DW.DeadlineDetails;
$(document).ready(function() {
    deadlineDetails.init();
    $(deadlineDetails.deadlineEnabledControl).change(function(){
        deadlineDetails.init();
    });
    $(deadlineDetails.frequencyPeriodControl).change(function(){
        deadlineDetails.show();
    });
});
