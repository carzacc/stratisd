// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

/// Macro for early return with Ok dbus message on failure to get data
/// associated with object path.
macro_rules! get_data {
    ($path:ident; $default:expr; $message:expr) => {
        if let Some(ref data) = *$path.get_data() {
            data
        } else {
            let message = format!("no data for object path {}", $path.get_name());
            let (rc, rs) = (u16::from(DbusErrorEnum::INTERNAL_ERROR), message);
            return Ok(vec![$message.append3($default, rc, rs)]);
        }
    };
}

/// Macro for early return with Ok dbus message on failure to get parent
/// object path from tree.
macro_rules! get_parent {
    ($m:ident; $data:ident; $default:expr; $message:expr) => {
        if let Some(parent) = $m.tree.get(&$data.parent) {
            parent
        } else {
            let message = format!("no path for object path {}", $data.parent);
            let (rc, rs) = (u16::from(DbusErrorEnum::INTERNAL_ERROR), message);
            return Ok(vec![$message.append3($default, rc, rs)]);
        }
    };
}

/// Macro for early return with Ok dbus message on failure to get mutable pool.
macro_rules! get_mut_pool {
    ($engine:ident; $uuid:ident; $default:expr; $message:expr) => {
        if let Some(pool) = $engine.get_mut_pool($uuid) {
            pool
        } else {
            let message = format!("engine does not know about pool with uuid {}", $uuid);
            let (rc, rs) = (u16::from(DbusErrorEnum::INTERNAL_ERROR), message);
            return Ok(vec![$message.append3($default, rc, rs)]);
        }
    };
}
