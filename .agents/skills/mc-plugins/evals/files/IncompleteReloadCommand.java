package com.example.crops.command;

import com.example.crops.manager.ConfigManager;
import com.example.crops.manager.HarvestDataManager;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

public class CropBoosterCommand implements CommandExecutor {
    private final ConfigManager configManager;
    private final HarvestDataManager harvestDataManager;

    public CropBoosterCommand(ConfigManager configManager, HarvestDataManager harvestDataManager) {
        this.configManager = configManager;
        this.harvestDataManager = harvestDataManager;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (args.length == 0) return false;

        if (args[0].equalsIgnoreCase("reload")) {
            if (!sender.hasPermission("cropbooster.reload")) {
                sender.sendMessage("No permission.");
                return true;
            }
            configManager.reload();
            sender.sendMessage("CropBooster configuration reloaded!");
            return true;
        }

        if (args[0].equalsIgnoreCase("save")) {
            if (!sender.hasPermission("cropbooster.save")) {
                sender.sendMessage("No permission.");
                return true;
            }
            configManager.save();
            harvestDataManager.save();
            sender.sendMessage("CropBooster data saved!");
            return true;
        }

        return false;
    }
}
