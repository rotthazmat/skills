package com.example.crops.manager;

import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.plugin.Plugin;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class ConfigManager {
    private final Plugin plugin;
    private final File configFile;
    private FileConfiguration config;

    private static final String CONFIG_HEADER =
        "# config.yml - CropBooster Settings\n" +
        "#\n" +
        "# growth-multiplier: <double>  # multiplier applied to crop growth ticks\n" +
        "# enabled-worlds: <list>       # worlds where boosting is active\n" +
        "#\n";

    public ConfigManager(Plugin plugin, File configFile, FileConfiguration config) {
        this.plugin = plugin;
        this.configFile = configFile;
        this.config = config;
    }

    public void saveConfigWithHeader() {
        try (FileWriter fw = new FileWriter(configFile)) {
            fw.write(CONFIG_HEADER);
        } catch (IOException e) {
            plugin.getLogger().severe("Could not save config: " + e.getMessage());
        }
    }

    public double getGrowthMultiplier() {
        return config.getDouble("growth-multiplier", 1.0);
    }

    public void setGrowthMultiplier(double value) {
        config.set("growth-multiplier", value);
        saveConfigWithHeader();
    }
}
