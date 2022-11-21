// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'resource.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

class ResourceAdapter extends TypeAdapter<Resource> {
  @override
  final int typeId = 1;

  @override
  Resource read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return Resource(
      id: fields[0] as int,
      title: fields[1] as String,
      url: fields[2] as String,
      publishedOn: fields[7] as String?,
      authors: fields[3] as String?,
      tags: fields[4] as String?,
      description: fields[5] as String?,
      thumbnail: fields[6] as String?,
      sourceId: fields[8] as int?,
      source: fields[9] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, Resource obj) {
    writer
      ..writeByte(10)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.title)
      ..writeByte(2)
      ..write(obj.url)
      ..writeByte(3)
      ..write(obj.authors)
      ..writeByte(4)
      ..write(obj.tags)
      ..writeByte(5)
      ..write(obj.description)
      ..writeByte(6)
      ..write(obj.thumbnail)
      ..writeByte(7)
      ..write(obj.publishedOn)
      ..writeByte(8)
      ..write(obj.sourceId)
      ..writeByte(9)
      ..write(obj.source);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ResourceAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
