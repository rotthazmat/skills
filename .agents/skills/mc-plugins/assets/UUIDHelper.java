package com.example.plugin.util;

import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.plugin.Plugin;

import java.lang.reflect.Method;

/**
 * Resolves a player's real UUID using OnlineIdentityChecker (OIC) if it is
 * installed and enabled, falling back to the vanilla session UUID otherwise.
 *
 * Adapt the package name and log prefix ("[PluginName]") to the target plugin;
 * the resolution logic itself should not change between plugins.
 */
public class UUIDHelper {

    private static Plugin onlineIdentityChecker;
    private static Method getUUIDFromNameMethod;
    private static boolean checkerAvailable = false;

    /**
     * Call once from onEnable(), after softdepend plugins have loaded.
     */
    public static void initialize() {
        Plugin plugin = Bukkit.getPluginManager().getPlugin("OnlineIdentityChecker");
        if (plugin != null && plugin.isEnabled()) {
            onlineIdentityChecker = plugin;
            try {
                getUUIDFromNameMethod = onlineIdentityChecker.getClass().getMethod("getUUIDFromName", String.class);
                checkerAvailable = true;
                Bukkit.getLogger().info("[PluginName] OnlineIdentityChecker integration enabled");
            } catch (NoSuchMethodException e) {
                Bukkit.getLogger().warning("[PluginName] OnlineIdentityChecker found but couldn't access getUUIDFromName method");
                checkerAvailable = false;
            }
        } else {
            Bukkit.getLogger().info("[PluginName] OnlineIdentityChecker not found, using legacy UUID method");
            checkerAvailable = false;
        }
    }

    /**
     * Gets the real UUID of an online player. Returns String, not UUID —
     * every plugin in this ecosystem stores this value as a String map key.
     */
    public static String getRealUUID(Player player) {
        if (checkerAvailable && onlineIdentityChecker != null && getUUIDFromNameMethod != null) {
            try {
                Object result = getUUIDFromNameMethod.invoke(onlineIdentityChecker, player.getName());
                if (result instanceof String) {
                    return (String) result;
                }
            } catch (Exception e) {
                Bukkit.getLogger().warning("[PluginName] Failed to get real UUID, falling back to legacy method: " + e.getMessage());
            }
        }

        return player.getUniqueId().toString();
    }

    /**
     * Resolves an offline player's UUID by name — for command targets who
     * aren't currently online. Extend here rather than duplicating fallback
     * logic in command handlers.
     */
    public static String getUUIDFromName(String playerName) {
        if (checkerAvailable && onlineIdentityChecker != null && getUUIDFromNameMethod != null) {
            try {
                Object result = getUUIDFromNameMethod.invoke(onlineIdentityChecker, playerName);
                if (result instanceof String) {
                    return (String) result;
                }
            } catch (Exception e) {
                Bukkit.getLogger().warning("[PluginName] Failed to get UUID for " + playerName + ", falling back to legacy method: " + e.getMessage());
            }
        }

        return Bukkit.getOfflinePlayer(playerName).getUniqueId().toString();
    }
}
