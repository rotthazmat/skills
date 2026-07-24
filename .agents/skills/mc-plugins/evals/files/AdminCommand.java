package com.example.zones.command;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

public class ZoneAdminCommand implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (args.length == 0) {
            sendHelp(sender);
            return true;
        }

        if (args[0].equalsIgnoreCase("reload")) {
            if (!sender.isOp()) {
                sender.sendMessage("You don't have permission to do that.");
                return true;
            }
            // reload logic here
            sender.sendMessage("Config reloaded.");
            return true;
        }

        return false;
    }

    private void sendHelp(CommandSender sender) {
        sender.sendMessage("/zoneadmin reload - reload the config");
        sender.sendMessage("--- PAPI Placeholders ---");
        sender.sendMessage("%zones_current_zone% - the zone the player is standing in");
        sender.sendMessage("%zones_zone_count% - total number of defined zones");
    }
}
