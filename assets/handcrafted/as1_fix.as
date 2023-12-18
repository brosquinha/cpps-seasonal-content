function sendMove(x, y)
{
   ENGINE.sendPlayerMove(x,y);
}
function getChildrenOf(target, recursive)
{
   var _loc3_ = [];
   for(var _loc4_ in target)
   {
      if(target[_loc4_] instanceof MovieClip)
      {
         _loc3_.push(target[_loc4_]);
         if(recursive)
         {
            _loc3_ = _loc3_.concat(getChildrenOf(target[_loc4_],true));
         }
      }
   }
   return _loc3_;
}
function setTriggers()
{
   var triggers = getChildrenOf(trigger,true);
   var i = 0;
   while(i < triggers.length)
   {
      var _loc3_ = triggers[i];
      _loc3_.triggerFunction = function()
      {
         if(this.name == "item")
         {
            INTERFACE.buyInventory(this.value.ItemId);
         }
         else if(this.name == "door")
         {
            var _loc2_ = !this.value.roomId ? roomNames[lowercase(this.value.room)] : SHELL.getRoomNameById(this.value.roomId);
            var _loc3_ = !this.value.newx ? 300 : this.value.newx;
            var _loc4_ = !this.value.newy ? 300 : this.value.newy;
            ENGINE.sendJoinRoom(_loc2_,_loc3_,_loc4_);
         }
      };
      i++;
   }
}
function lowercase(str)
{
   return str.split(" ").join("").toLowerCase();
}
var ENGINE = _global.getCurrentEngine();
var INTERFACE = _global.getCurrentInterface();
var SHELL = _global.getCurrentShell();
var roomNames = {town:"town",dancelounge:"lounge",snowforts:"forts",coffeeshop:"coffee",danceclub:"dance",dock:"dock",shop:"shop",mtn:"mtn",sportshop:"sport",skihill:"village"};
var start_x = 0;
var start_y = 0;
ENGINE.setRoomBlockMovieClip(block);
ENGINE.setRoomTriggersMovieClip(trigger);
foreground.swapDepths(900001);
_root.mySetup.isShip = SHELL.isMigratorHere();
block._visible = false;
trigger._visible = false;
setTriggers();
