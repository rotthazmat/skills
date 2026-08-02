package com.example.plugin.manager;

import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.Plugin;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Reference implementation of the header-survival pattern for two related
 * YAML files. Copy the shape (header constant, load, save, reload,
 * writeWithHeader) — substitute the actual fields for the target plugin's
 * data.
 */
public class DataManager {
    private final Plugin plugin;
    private final File playersFile;
    private FileConfiguration playersConfig;

    private static final String PLAYERS_HEADER =
        "# players.yml - <Plugin> Player Data\n" +
        "#\n" +
        "# Structure:\n" +
        "# players:\n" +
        "#   <uuid>:\n" +
        "#     balance: <double>   # example field — replace with real schema\n" +
        "#\n";

    private final Map<String, Double> balances = new HashMap<>();

    public DataManager(Plugin plugin) {
        this.plugin = plugin;
        this.playersFile = new File(plugin.getDataFolder(), "players.yml");
        loadData();
    }

    private void loadData() {
        plugin.getDataFolder().mkdirs();
        if (!playersFile.exists()) plugin.saveResource("players.yml", false);
        playersConfig = YamlConfiguration.loadConfiguration(playersFile);

        // Clear before repopulating — this method also backs reload(), which
        // must replace in-memory state rather than merge into stale entries.
        balances.clear();
        ConfigurationSection section = playersConfig.getConfigurationSection("players");
        if (section != null) {
            for (String uuid : section.getKeys(false)) {
                balances.put(uuid, section.getDouble(uuid + ".balance", 0.0));
            }
        }
    }

    /**
     * Re-reads players.yml from disk, replacing all in-memory state — the
     * inverse of save(). The plugin's /‹command› reload subcommand must call
     * this on every manager instance it holds, not just a config manager.
     */
    public void reload() {
        loadData();
    }

    public void save() {
        playersConfig.set("players", null);
        for (Map.Entry<String, Double> entry : balances.entrySet()) {
            playersConfig.set("players." + entry.getKey() + ".balance", entry.getValue());
        }
        writeWithHeader(playersFile, playersConfig, PLAYERS_HEADER);
    }

    /**
     * Always merge saveToString() before prepending the header — writing the
     * header string alone silently discards every real value in the file.
     */
    private void writeWithHeader(File file, FileConfiguration config, String header) {
        String yaml = config.saveToString().replaceAll("(?m)^#[^\\n]*\\n?", "");
        try (FileWriter fw = new FileWriter(file)) {
            fw.write(header + yaml);
        } catch (IOException e) {
            plugin.getLogger().severe("Could not save " + file.getName() + ": " + e.getMessage());
        }
    }

    public double getBalance(String uuid) {
        return balances.getOrDefault(uuid, 0.0);
    }

    public void setBalance(String uuid, double amount) {
        balances.put(uuid, amount);
        save();
    }
}
