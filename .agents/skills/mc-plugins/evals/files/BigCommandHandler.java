package com.example.zones.command;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public class ZoneCommandExecutor implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (args.length == 0) return false;
        String sub = args[0].toLowerCase();

        if (sub.equals("create")) {
            // ~30 lines: parse name, corners, validate overlap, persist to YAML
            return true;
        } else if (sub.equals("delete")) {
            // ~25 lines: look up zone, confirm ownership, remove from YAML
            return true;
        } else if (sub.equals("setwarp")) {
            // ~30 lines: parse location args, validate world, store warp
            return true;
        } else if (sub.equals("seticon")) {
            // ~20 lines: parse material name, validate, store icon
            return true;
        } else if (sub.equals("enable")) {
            // ~15 lines
            return true;
        } else if (sub.equals("disable")) {
            // ~15 lines
            return true;
        } else if (sub.equals("addplayer")) {
            // ~25 lines: resolve player name to UUID inline, add to whitelist
            return true;
        } else if (sub.equals("removeplayer")) {
            // ~25 lines
            return true;
        } else if (sub.equals("list")) {
            // ~20 lines
            return true;
        } else if (sub.equals("info")) {
            // ~20 lines
            return true;
        }
        // ...12 more subcommands follow this same inline pattern in the real file,
        // pushing it past 800 lines total...
        return false;
    }
}
