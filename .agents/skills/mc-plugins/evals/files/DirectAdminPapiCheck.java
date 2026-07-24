package com.example.zones.command;

import org.bukkit.ChatColor;
import org.bukkit.command.CommandSender;

public class ZoneHelp {
    public static void sendHelp(CommandSender sender) {
        sender.sendMessage(ChatColor.GOLD + "--- Zones Help (/zones) ---");
        sender.sendMessage(ChatColor.WHITE + "/zones list" + ChatColor.GRAY + " - list all zones");

        if (sender.hasPermission("zones.admin")) {
            sender.sendMessage(ChatColor.RED + "--- Server Admin Commands ---");
            sender.sendMessage(ChatColor.WHITE + "/zones reload" + ChatColor.GRAY + " - reload configuration");

            sender.sendMessage(ChatColor.LIGHT_PURPLE + "--- PAPI Placeholders ---");
            sender.sendMessage(ChatColor.WHITE + "%zones_current_zone%" + ChatColor.GRAY + " - the zone the player is standing in");
        }
    }
}
